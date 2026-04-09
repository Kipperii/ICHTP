/* similarity-pipeline.js
 * 提供跨遊戲共用的圖片變體評估與生成管線：
 *  - 分層混合多種特徵：aHash / 直方圖差 / MSE / SSIM / ORB
 *  - 難度自適應閾值 (線性或自訂插值)
 *  - 權重可配置
 *  - 特徵快取與變體去重
 *
 * 公開介面：
 *   SimilarityPipeline.init()
 *   SimilarityPipeline.extractOrig(scene, answerKey)  // 建立 / 取得原圖特徵
 *   SimilarityPipeline.evaluateVariant(origFeat, variantCanvas, acceptedHashes, difficulty)
 *   SimilarityPipeline.generateVariants(scene, answerKey, count, difficulty)  // 方便沿用舊介面
 *
 * evaluateVariantAdvanced(origFeat, variantCanvas, acceptedHashes, difficulty) 保持語意：
 *   回傳 { reject:boolean, meta?:{ mse, hdiff, ssim, orbCount, orbGood, aHashHam, aHash, simScore } }
 */

(function(global){
  const SP = {};

  /* ================== Config ================== */
  const defaultWeights = {
    mseW: 0.05,
    hdiffW: 0.15,
    ssimW: 0.40,
    aiW: 0.30,
    orbW: 0.00,
    diversityW: 0.10
  };

  // 線性區間 (difficulty d 介於 0.1~0.95)
  const defaultRanges = {
    mse:   { min:  90, max: 2600 },       // 原始 MSE (RGB sum) 可接受範圍
    hist:  { min:  0.08, max: 0.42 },     // 直方圖 (L1) 差異
    ssim:  { min:  0.55, max: 0.88 },     // SSIM 或推估值
    ham:   { min:  8, max: 26 },          // aHash 漢明距離（大表示差異度高）
    orb:   { min:  6, max: 42 }           // 好的 ORB match 數
  };

  // 可注入自訂插值函式：f(d)→數值
  const interpolate = {
    mseMin: (d)=>lerp(defaultRanges.mse.min*0.7, defaultRanges.mse.min, d),
    mseMax: (d)=>lerp(defaultRanges.mse.max*0.85, defaultRanges.mse.max, d),
    histMin:(d)=>lerp(defaultRanges.hist.min*0.6, defaultRanges.hist.min, d),
    histMax:(d)=>lerp(defaultRanges.hist.max*0.85, defaultRanges.hist.max, d),
    ssimMin:(d)=>lerp(defaultRanges.ssim.min*0.9, defaultRanges.ssim.min, d),
    ssimMax:(d)=>lerp(defaultRanges.ssim.max*0.95, defaultRanges.ssim.max, d),
    hamMin: (d)=>lerp(defaultRanges.ham.min*0.9, defaultRanges.ham.min, d),
    hamMax: (d)=>lerp(defaultRanges.ham.max*0.9, defaultRanges.ham.max, d),
    orbMin: (d)=>lerp(defaultRanges.orb.min*0.9, defaultRanges.orb.min, d),
    orbMax: (d)=>lerp(defaultRanges.orb.max*0.85, defaultRanges.orb.max, d)
  };

  // 分段通過分數（融合後）區間，難度高要求更嚴
  const scorePassLow = (d)=>lerp(0.28, 0.35, d);   // 下限
  const scorePassHigh= (d)=>lerp(0.72, 0.82, d);   // 高品質直接接受

  SP.config = {
    weights: { ...defaultWeights },
    interpolate,
    enabled: true
  };

  SP.setWeights = (w)=>Object.assign(SP.config.weights, w||{});
  SP.setInterpolator = (name, fn)=>{
    if(name in SP.config.interpolate && typeof fn==='function'){
      SP.config.interpolate[name]=fn;
    }
  };

  /* ================== Caches ================== */
  const origFeatCache = new Map();
  const variantMetaCache = new Map();
  const seenVariantSignature = new Set();

  SP.resetCaches = ()=>{
    // Dispose tensors in cache
    for(const feat of origFeatCache.values()){
      if(feat.aiEmbedding && feat.aiEmbedding.dispose){
        feat.aiEmbedding.dispose();
      }
    }
    origFeatCache.clear();
    variantMetaCache.clear();
    seenVariantSignature.clear();
  };

  /* ================== AI Model ================== */
  SP.aiModel = null;
  let isModelLoading = false;

  SP.loadAIModel = async function(){
    if(SP.aiModel) return SP.aiModel;
    if(isModelLoading) return null;
    if(typeof mobilenet === 'undefined' || typeof tf === 'undefined'){
      console.warn('TensorFlow.js or MobileNet not loaded');
      return null;
    }
    isModelLoading = true;
    try{
      SP.aiModel = await mobilenet.load({version: 2, alpha: 1.0});
      
      // --- Performance Optimization: Warm Up ---
      // Execute a dummy inference to compile WebGL shaders immediately.
      // This prevents the "lag" (freeze) during the first gameplay interaction.
      tf.tidy(() => {
        const output = SP.aiModel.infer(tf.zeros([1, 224, 224, 3]), true);
      });
      console.log('MobileNet loaded & Warmed up (Performance Optimization Applied)');
      
      return SP.aiModel;
    }catch(e){
      console.error('AI Model load failed', e);
      return null;
    }finally{
      isModelLoading = false;
    }
  };

  function getAIEmbedding(model, canvas){
    if(!model) return null;
    // infer(img, embedding=true) returns the embedding tensor
    return model.infer(canvas, true);
  }

  function cosineSimilarity(tensorA, tensorB){
    if(!tensorA || !tensorB) return 0;
    return tf.tidy(()=>{
      const dotProduct = tf.sum(tf.mul(tensorA, tensorB));
      const normA = tf.norm(tensorA);
      const normB = tf.norm(tensorB);
      const similarity = tf.div(dotProduct, tf.mul(normA, normB));
      return similarity.dataSync()[0];
    });
  }

  /* ================== Utils ================== */
  function lerp(a,b,t){ return a + (b-a)*Math.max(0,Math.min(1,t)); }
  function clamp(v,min,max){ return v<min?min:v>max?max:v; }
  function canvasFromImage(img){
    const c=document.createElement('canvas');
    c.width=img.naturalWidth||img.width;
    c.height=img.naturalHeight||img.height;
    c.getContext('2d').drawImage(img,0,0);
    return c;
  }
  function sampleCanvasRGB(canvas, w=64,h=64){
    const c=document.createElement('canvas'); c.width=w; c.height=h;
    const ctx=c.getContext('2d',{willReadFrequently:true});
    ctx.drawImage(canvas,0,0,w,h);
    return ctx.getImageData(0,0,w,h).data;
  }
  function computeMSE(sampleA, canvasB){
    const w=64,h=64;
    const c=document.createElement('canvas'); c.width=w; c.height=h;
    const ctx=c.getContext('2d',{willReadFrequently:true});
    ctx.drawImage(canvasB,0,0,w,h);
    const b=ctx.getImageData(0,0,w,h).data;
    let mse=0,n=0;
    for(let i=0;i<b.length;i+=4){
      const da=sampleA[i]-b[i];
      const db=sampleA[i+1]-b[i+1];
      const dc=sampleA[i+2]-b[i+2];
      mse += da*da + db*db + dc*dc;
      n++;
    }
    return mse/Math.max(1,n);
  }
  function computeGrayHist(canvas, bins=64){
    const w=canvas.width, h=canvas.height;
    const ctx=canvas.getContext('2d',{willReadFrequently:true});
    const data=ctx.getImageData(0,0,w,h).data;
    const hist=new Array(bins).fill(0);
    for(let i=0;i<data.length;i+=4){
      const g = (data[i]*0.299 + data[i+1]*0.587 + data[i+2]*0.114)|0;
      const idx = Math.min(bins-1, (g/256*bins)|0);
      hist[idx]++;
    }
    const tot = hist.reduce((a,b)=>a+b,0);
    return hist.map(v=>v/tot);
  }
  function histDiff(h1,h2){
    let d=0;
    for(let i=0;i<h1.length;i++) d += Math.abs(h1[i]-h2[i]);
    return d;
  }
  function computeAHash(canvas){
    const size=8;
    const c=document.createElement('canvas');c.width=size;c.height=size;
    const ctx=c.getContext('2d',{willReadFrequently:true});
    ctx.drawImage(canvas,0,0,size,size);
    const data=ctx.getImageData(0,0,size,size).data;
    let sum=0; const gray=[];
    for(let i=0;i<data.length;i+=4){
      const g=(data[i]*0.299 + data[i+1]*0.587 + data[i+2]*0.114);
      gray.push(g); sum+=g;
    }
    const avg=sum/gray.length;
    let bits='';
    for(const g of gray) bits += g>avg?'1':'0';
    let hex='';
    for(let i=0;i<bits.length;i+=4){
      hex += parseInt(bits.slice(i,i+4),2).toString(16);
    }
    return hex;
  }
  function hammingHash(h1,h2){
    if(!h1||!h2||h1.length!==h2.length) return 64;
    let dist=0;
    for(let i=0;i<h1.length;i++){
      if(h1[i]!==h2[i]) dist++;
    }
    return dist;
  }

  function computeORB(canvas){
    if(typeof cv==='undefined' || !cv.ORB) return {orbCount:0, orbGood:0};
    try{
      const mat=cv.imread(canvas);
      const gray=new cv.Mat();
      cv.cvtColor(mat, gray, cv.COLOR_RGBA2GRAY);
      const orb=cv.ORB.create();
      const kp=new cv.KeyPointVector();
      const desc=new cv.Mat();
      orb.detectAndCompute(gray,new cv.Mat(),kp,desc);
      const orbCount=kp.size();
      mat.delete(); gray.delete();
      return {desc, orbCount};
    }catch(e){
      return {orbCount:0, orbGood:0};
    }
  }

  function matchORB(descA, canvasB){
    if(!descA || typeof cv==='undefined' || !cv.ORB) return {orbCount:0, orbGood:0};
    try{
      const mat=cv.imread(canvasB);
      const gray=new cv.Mat();
      cv.cvtColor(mat, gray, cv.COLOR_RGBA2GRAY);
      const orb=cv.ORB.create();
      const kpB=new cv.KeyPointVector();
      const descB=new cv.Mat();
      orb.detectAndCompute(gray,new cv.Mat(),kpB,descB);
      const orbCount = kpB.size();
      if(!descB.rows){
        mat.delete(); gray.delete(); kpB.delete(); descB.delete();
        return {orbCount:0, orbGood:0};
      }
      const bf=new cv.BFMatcher(cv.NORM_HAMMING, true);
      const matches=new cv.DMatchVector();
      bf.match(descA, descB, matches);
      let orbGood=0;
      for(let i=0;i<matches.size();i++){
        const m=matches.get(i);
        if(m.distance <= 42) orbGood++;
      }
      mat.delete(); gray.delete(); kpB.delete(); descB.delete(); matches.delete(); bf.delete();
      return {orbCount, orbGood};
    }catch(e){
      return {orbCount:0, orbGood:0};
    }
  }

  function computeSSIM(canvasA, canvasB){
    const w=64, h=64;
    const cA=document.createElement('canvas'); cA.width=w; cA.height=h;
    const ctxA=cA.getContext('2d',{willReadFrequently:true});
    ctxA.drawImage(canvasA,0,0,w,h);
    const dataA=ctxA.getImageData(0,0,w,h).data;

    const cB=document.createElement('canvas'); cB.width=w; cB.height=h;
    const ctxB=cB.getContext('2d',{willReadFrequently:true});
    ctxB.drawImage(canvasB,0,0,w,h);
    const dataB=ctxB.getImageData(0,0,w,h).data;

    const lumaA = new Float32Array(w*h);
    const lumaB = new Float32Array(w*h);
    for(let i=0; i<w*h; i++){
      lumaA[i] = 0.299*dataA[i*4] + 0.587*dataA[i*4+1] + 0.114*dataA[i*4+2];
      lumaB[i] = 0.299*dataB[i*4] + 0.587*dataB[i*4+1] + 0.114*dataB[i*4+2];
    }

    const K1=0.01, K2=0.03, L=255;
    const C1=(K1*L)**2, C2=(K2*L)**2;
    
    const winSize=8;
    let mssimSum=0, count=0;

    for(let y=0; y<=h-winSize; y+=winSize){
      for(let x=0; x<=w-winSize; x+=winSize){
        let muA=0, muB=0;
        let sumA2=0, sumB2=0, sumAB=0;
        
        for(let dy=0; dy<winSize; dy++){
          for(let dx=0; dx<winSize; dx++){
            const idx = (y+dy)*w + (x+dx);
            const va = lumaA[idx];
            const vb = lumaB[idx];
            muA += va;
            muB += vb;
            sumA2 += va*va;
            sumB2 += vb*vb;
            sumAB += va*vb;
          }
        }
        
        const N = winSize*winSize;
        muA /= N;
        muB /= N;
        
        const sigmaA2 = (sumA2/N) - muA*muA;
        const sigmaB2 = (sumB2/N) - muB*muB;
        const sigmaAB = (sumAB/N) - muA*muB;
        
        const ssim = ((2*muA*muB + C1)*(2*sigmaAB + C2)) / 
                     ((muA*muA + muB*muB + C1)*(sigmaA2 + sigmaB2 + C2));
        
        mssimSum += ssim;
        count++;
      }
    }
    return count>0 ? mssimSum/count : 0;
  }

  /* ================== Extraction ================== */
  SP.extractOrig = function(scene, answerKey){
    if(origFeatCache.has(answerKey)) return origFeatCache.get(answerKey);
    const tex = scene.textures.get(answerKey);
    if(!tex) return null;
    const img = tex.getSourceImage();
    const canvas = canvasFromImage(img);
    const aHash = computeAHash(canvas);
    const hist = computeGrayHist(canvas);
    const sample = sampleCanvasRGB(canvas);
    let orb = computeORB(canvas);
    let orbDesc = orb.desc || null;
    
    let aiEmbedding = null;
    if(SP.aiModel){
      aiEmbedding = getAIEmbedding(SP.aiModel, canvas);
    }

    const feat = {
      key: answerKey,
      canvas,
      aHash,
      hist,
      sample,
      orbDesc,
      orbKeypoints: orb.orbCount||0,
      aiEmbedding
    };
    origFeatCache.set(answerKey, feat);
    return feat;
  };

  /* ================== Evaluation ================== */
  function evaluateVariantAdvanced(origFeat, variantCanvas, acceptedHashes, difficulty){
    if(!SP.config.enabled || !origFeat || !variantCanvas){
      return {reject:true};
    }
    const d = clamp(difficulty||0.5,0.05,1);

    const vHash = computeAHash(variantCanvas);
    if(acceptedHashes && acceptedHashes.some(h=>hammingHash(h,vHash)<4)){
      return {reject:true, meta:{aHash:vHash, aHashHam:0}};
    }

    const hamToOrig = hammingHash(origFeat.aHash, vHash);
    const vHist = computeGrayHist(variantCanvas);
    const hdiff = histDiff(origFeat.hist, vHist);
    const mse = computeMSE(origFeat.sample, variantCanvas);
    const ssim = computeSSIM(origFeat.canvas, variantCanvas);

    // [Fix] Strict pixel-level hard-reject to prevent near-identical distractors.
    // Thresholds raised to ensure every distractor has a clearly visible difference.
    if(hamToOrig <= 2 || (mse < 200 && ssim > 0.94) || (hdiff < 0.06 && mse < 200)) {
        return {reject:true, meta:{aHash:vHash, aHashHam:hamToOrig, mse, ssim, simScore:1.0, note:"Too similar to original"}};
    }

    let aiScore = 0;
    if(SP.aiModel && origFeat.aiEmbedding){
      const vEmb = getAIEmbedding(SP.aiModel, variantCanvas);
      aiScore = cosineSimilarity(origFeat.aiEmbedding, vEmb);
      
      // [Fix] AI-based Hard Reject — MobileNet cosine similarity threshold
      if(aiScore > 0.85) {
         if(vEmb) vEmb.dispose();
         return {reject:true, meta:{aHash:vHash, aHashHam:hamToOrig, mse, ssim, aiScore, simScore:1.0, note:"AI says too similar"}};
      }

      if(vEmb) vEmb.dispose();
    }
    aiScore = clamp(aiScore, 0, 1);

    let orbCount=0, orbGood=0;
    if(typeof cv!=='undefined' && cv.ORB && origFeat.orbDesc){
      const orbRes = matchORB(origFeat.orbDesc, variantCanvas);
      orbCount = orbRes.orbCount;
      orbGood  = orbRes.orbGood;
    }

    const mseMin = interpolate.mseMin(d), mseMax=interpolate.mseMax(d);
    const histMin=interpolate.histMin(d), histMax=interpolate.histMax(d);
    const ssimMin=interpolate.ssimMin(d), ssimMax=interpolate.ssimMax(d);
    const hamMin = interpolate.hamMin(d), hamMax = interpolate.hamMax(d);
    const orbMin = interpolate.orbMin(d), orbMax = interpolate.orbMax(d);

    const mseScore  = 1 - clamp((mse - mseMin)/(mseMax - mseMin),0,1);
    const hdiffScore= 1 - clamp((hdiff - histMin)/(histMax - histMin),0,1);
    const ssimScore = clamp((ssim - ssimMin)/(ssimMax - ssimMin),0,1);
    const orbScore  = clamp((orbGood - orbMin)/(orbMax - orbMin),0,1);
    const diversityScore = clamp((hamToOrig - hamMin)/(hamMax - hamMin),0,1);

    const {mseW, hdiffW, ssimW, orbW, diversityW, aiW} = SP.config.weights;
    const simScore = (
      mseScore * mseW +
      hdiffScore * hdiffW +
      ssimScore * ssimW +
      orbScore * orbW +
      diversityScore * diversityW +
      aiScore * (aiW||0)
    );

    let reject;
    if(simScore >= scorePassHigh(d)){
      reject = false;
    }else if(simScore < scorePassLow(d)){
      reject = true;
    }else{
      reject = false;
    }

    const meta={mse,hdiff,ssim,orbCount,orbGood,aHashHam:hamToOrig,aHash:vHash,simScore,aiScore};
    return {reject, meta};
  }

  SP.evaluateVariant = function(origFeat, variantCanvas, acceptedHashes, difficulty){
    return evaluateVariantAdvanced(origFeat, variantCanvas, acceptedHashes||[], difficulty);
  };

  /* ================== Variant Generation (簡易) ================== */
  SP.generateVariants = async function(scene, answerKey, count, difficulty){
    const tex = scene.textures.get(answerKey);
    if(!tex) return [];
    const img = tex.getSourceImage();
    const orig = SP.extractOrig(scene, answerKey);
    const accepted = [];
    const acceptedHashes = [];
    const acceptedCanvases = [];     // for pixel-level inter-variant check
    const acceptedEmbeddings = [];   // for AI inter-variant check
    const triesLimit = Math.max(count*15, 35);  // raised for stricter filtering
    let tries=0;

    while(accepted.length < count && tries < triesLimit){
      tries++;
      const canvas = genVariantCanvasBasic(img, difficulty);
      const signature = answerKey + '|' + canvas.width + 'x' + canvas.height + '|' + canvas._sig;
      if(seenVariantSignature.has(signature)) continue;
      const ev = SP.evaluateVariant(orig, canvas, acceptedHashes, difficulty);
      if(ev.reject) continue;

      // --- Inter-variant deduplication ---
      let tooSimilarToAccepted = false;

      if(SP.aiModel){
        // AI-based: compare MobileNet embeddings with all accepted variants
        const vEmb = getAIEmbedding(SP.aiModel, canvas);
        if(vEmb){
          for(const accEmb of acceptedEmbeddings){
            if(cosineSimilarity(accEmb, vEmb) > 0.85){
              tooSimilarToAccepted = true;
              break;
            }
          }
          if(tooSimilarToAccepted){
            vEmb.dispose();
          } else {
            acceptedEmbeddings.push(vEmb);
          }
        }
      } else {
        // Fallback: pixel-level MSE check between variants
        const candSample = sampleCanvasRGB(canvas);
        for(const accCanvas of acceptedCanvases){
          if(computeMSE(candSample, accCanvas) < 180){
            tooSimilarToAccepted = true;
            break;
          }
        }
      }

      if(tooSimilarToAccepted) continue;

      acceptedCanvases.push(canvas);
      variantMetaCache.set(signature, ev.meta);
      seenVariantSignature.add(signature);
      const key = 'var:' + Date.now() + '-' + Math.random().toString(36).slice(2,7);
      try{
        const url = canvas.toDataURL('image/png');
        const im = new Image();
        im.crossOrigin='anonymous';
        await new Promise((res,rej)=>{
          im.onload=()=>res();
          im.onerror=()=>rej(new Error('img load fail'));
          im.src=url;
        });
        if(!scene.textures.exists(key)){
          scene.textures.addImage(key, im);
        }
        accepted.push(key);
        acceptedHashes.push(ev.meta.aHash);
      }catch(e){
      }
    }

    // Clean up inter-variant AI embeddings
    acceptedEmbeddings.forEach(e=>{ if(e && e.dispose) e.dispose(); });

    return accepted;
  };

  function genVariantCanvasBasic(img, d){
    const w = img.naturalWidth || img.width;
    const h = img.naturalHeight || img.height;

    // New variant family: clone extracted object(s) onto blue background (2~5, non-overlap)
    if(Math.random() < lerp(0.20, 0.40, d)){
      const cloneVariant = genObjectCloneVariantCanvas(img, d);
      if(cloneVariant) return cloneVariant;
    }

    const c = document.createElement('canvas'); c.width=w; c.height=h;
    const ctx = c.getContext('2d', {willReadFrequently:true});

    ctx.fillStyle = avgColor(img);
    ctx.fillRect(0,0,w,h);

    const flipH = Math.random() < lerp(0.15,0.5,d);
    const flipV = Math.random() < lerp(0.08,0.3,d);
    // Mild transform combo: small rotation + perspective-like tilt (shear) + non-uniform scaling
    // Keep values conservative to avoid over-hard distractors.
    // Minimum deformation thresholds to avoid near-identical outputs
    let rotDeg = (Math.random()*2-1) * lerp(3.5, 6.0, d);
    const minRotDeg = lerp(2.2, 3.5, d);
    if(Math.abs(rotDeg) < minRotDeg) rotDeg = rotDeg >= 0 ? minRotDeg : -minRotDeg;
    const rotRad = rotDeg * Math.PI / 180;

    let dx = (Math.random()*2-1) * lerp(0.03, 0.06, d);
    let dy = (Math.random()*2-1) * lerp(0.03, 0.06, d);
    const minScaleDelta = lerp(0.02, 0.04, d);
    if(Math.abs(dx) < minScaleDelta) dx = dx >= 0 ? minScaleDelta : -minScaleDelta;
    if(Math.abs(dy) < minScaleDelta) dy = dy >= 0 ? minScaleDelta : -minScaleDelta;
    const sx = 1 + dx;
    const sy = 1 + dy;

    let tiltX = (Math.random()*2-1) * lerp(0.015, 0.04, d);
    let tiltY = (Math.random()*2-1) * lerp(0.01, 0.03, d);
    const minTiltX = lerp(0.010, 0.018, d);
    const minTiltY = lerp(0.008, 0.015, d);
    if(Math.abs(tiltX) < minTiltX) tiltX = tiltX >= 0 ? minTiltX : -minTiltX;
    if(Math.abs(tiltY) < minTiltY) tiltY = tiltY >= 0 ? minTiltY : -minTiltY;

    ctx.save();
    ctx.translate(w/2, h/2);
    ctx.transform(1, tiltY, tiltX, 1, 0, 0);
    ctx.rotate(rotRad);
    ctx.scale(flipH?-sx:sx, flipV?-sy:sy);
    ctx.drawImage(img, -w/2, -h/2, w, h);
    ctx.restore();

    if(Math.random()<lerp(0.12,0.35,d)){
      // Use safer blend modes only to avoid dark/inverted artifacts.
      ctx.globalCompositeOperation = pick(['screen','overlay','soft-light']);
      ctx.globalAlpha = clamp(lerp(0.12,0.30,d)+ (Math.random()*0.08-0.04),0.10,0.35);
      ctx.save();
      const f2h = Math.random()<0.5, f2v=Math.random()<0.3;
      ctx.translate(f2h?w:0, f2v?h:0);
      ctx.scale(f2h?-1:1, f2v?-1:1);
      // Keep offset small to reduce visible edge ghosting.
      const offX = (Math.random()*2-1)*lerp(3.5,1.6,d);
      const offY = (Math.random()*2-1)*lerp(3.5,1.6,d);
      ctx.drawImage(img, offX, offY);
      ctx.restore();
      ctx.globalAlpha = 1;
      ctx.globalCompositeOperation='source-over';
    }

    if(Math.random()<lerp(0.35,0.85,d)){
      const id = ctx.getImageData(0,0,w,h);
      const data = id.data;
      let hShift = (Math.random()*2-1)*lerp(45,15,d);
      // Guarantee minimum visible hue shift to avoid near-identical variants
      const minShift = lerp(18, 8, d);
      if(Math.abs(hShift) < minShift) hShift = hShift >= 0 ? minShift : -minShift;
      const sMul = 1 + (Math.random()*2-1)*lerp(0.18,0.08,d);
      for(let i=0;i<data.length;i+=4){
        if(data[i+3]<16) continue;
        let r=data[i]/255,g=data[i+1]/255,b=data[i+2]/255;
        let max=Math.max(r,g,b), min=Math.min(r,g,b);
        let h,s,v=max, dlt=max-min;
        s= max===0?0:dlt/max;
        if(dlt!==0){
          switch(max){
            case r: h=(g-b)/dlt + (g<b?6:0); break;
            case g: h=(b-r)/dlt + 2; break;
            case b: h=(r-g)/dlt + 4; break;
          }
          h/=6;
        }else h=0;
        h = (h + hShift/360 + 1)%1;
        s = clamp(s*sMul,0,1);
        const hi = Math.floor(h*6);
        const f = h*6 - hi;
        const p = v*(1-s);
        const q = v*(1-s*f);
        const t = v*(1-s*(1-f));
        let R,G,B;
        switch(hi%6){
          case 0: R=v; G=t; B=p; break;
          case 1: R=q; G=v; B=p; break;
          case 2: R=p; G=v; B=t; break;
          case 3: R=p; G=q; B=v; break;
          case 4: R=t; G=p; B=v; break;
          case 5: R=v; G=p; B=q; break;
        }
        data[i]  = (R*255)|0;
        data[i+1]= (G*255)|0;
        data[i+2]= (B*255)|0;
      }
      ctx.putImageData(id,0,0);
    }

    // Blur removed intentionally (low therapeutic value in current validation setup).

    const pad = Math.round(Math.random()*lerp(18,5,d));
    if(pad>0 && pad*2 < Math.min(w,h)){
      const tmp=document.createElement('canvas');
      tmp.width=w; tmp.height=h;
      tmp.getContext('2d').drawImage(c,pad,pad,w-2*pad,h-2*pad,0,0,w,h);
      return Object.assign(tmp,{_sig:`p${pad}`});
    }

    return Object.assign(c,{_sig:`${flipH?'H':''}${flipV?'V':''}`});
  }

  function genObjectCloneVariantCanvas(img, d){
    const w = img.naturalWidth || img.width;
    const h = img.naturalHeight || img.height;
    if(w <= 0 || h <= 0) return null;

    const src = document.createElement('canvas');
    src.width = w; src.height = h;
    const sctx = src.getContext('2d', {willReadFrequently:true});
    sctx.drawImage(img, 0, 0, w, h);

    // Simple chroma key to remove solid/gradient background (assuming top-left is background)
    // This perfectly cuts out the object from JPGs and avoids square bounding boxes!
    const imgD = sctx.getImageData(0, 0, w, h);
    const dArr = imgD.data;
    function getCol(x,y){ const i=(y*w+x)*4; return [dArr[i],dArr[i+1],dArr[i+2],dArr[i+3]]; }
    const TL = getCol(0,0), TR = getCol(w-1,0), BL = getCol(0,h-1), BR = getCol(w-1,h-1);

    // Flood-fill chroma key starting from edges to prevent internal object holes
    if(TL[3] > 10){
      const visited = new Uint8Array(w * h);
      let q = [];
      for(let x=0; x<w; x++){ q.push(x, 0); q.push(x, h-1); }
      for(let y=0; y<h; y++){ q.push(0, y); q.push(w-1, y); }
      let head = 0;
      while(head < q.length){
        const x = q[head++], y = q[head++];
        const idx = y * w + x;
        if(visited[idx]) continue;
        visited[idx] = 1;
        const tx = x / (w-1 || 1), ty = y / (h-1 || 1);
        const expR = TL[0] + (TR[0]-TL[0])*tx + (BL[0]-TL[0])*ty + (TL[0]-TR[0]-BL[0]+BR[0])*tx*ty;
        const expG = TL[1] + (TR[1]-TL[1])*tx + (BL[1]-TL[1])*ty + (TL[1]-TR[1]-BL[1]+BR[1])*tx*ty;
        const expB = TL[2] + (TR[2]-TL[2])*tx + (BL[2]-TL[2])*ty + (TL[2]-TR[2]-BL[2]+BR[2])*tx*ty;
        const pIdx = idx * 4;
        if(Math.abs(dArr[pIdx]-expR)<40 && Math.abs(dArr[pIdx+1]-expG)<40 && Math.abs(dArr[pIdx+2]-expB)<40){
          dArr[pIdx+3] = 0;
          if(x>0) q.push(x-1, y);
          if(x<w-1) q.push(x+1, y);
          if(y>0) q.push(x, y-1);
          if(y<h-1) q.push(x, y+1);
        }
      }
      sctx.putImageData(imgD, 0, 0);
    }

    const bounds = extractAlphaBounds(src, 18);
    if(!bounds) return null;

    const crop = document.createElement('canvas');
    crop.width = bounds.w;
    crop.height = bounds.h;
    crop.getContext('2d').drawImage(src, bounds.x, bounds.y, bounds.w, bounds.h, 0, 0, bounds.w, bounds.h);

    const out = document.createElement('canvas');
    out.width = w; out.height = h;
    const octx = out.getContext('2d', {willReadFrequently:true});
    
    // Synthesize a clean background gradient so we don't paste over the original object!
    const bgImgD = octx.createImageData(w, h);
    for(let y=0; y<h; y++){
      for(let x=0; x<w; x++){
        const tx = x / (w-1 || 1), ty = y / (h-1 || 1);
        const expR = TL[0] + (TR[0]-TL[0])*tx + (BL[0]-TL[0])*ty + (TL[0]-TR[0]-BL[0]+BR[0])*tx*ty;
        const expG = TL[1] + (TR[1]-TL[1])*tx + (BL[1]-TL[1])*ty + (TL[1]-TR[1]-BL[1]+BR[1])*tx*ty;
        const expB = TL[2] + (TR[2]-TL[2])*tx + (BL[2]-TL[2])*ty + (TL[2]-TR[2]-BL[2]+BR[2])*tx*ty;
        const idx = (y*w + x)*4;
        bgImgD.data[idx] = expR; bgImgD.data[idx+1] = expG; bgImgD.data[idx+2] = expB; bgImgD.data[idx+3] = 255;
      }
    }
    octx.putImageData(bgImgD, 0, 0);

    const targetCount = 2 + ((Math.random() * 2) | 0); // 2~3 items (fewer but bigger)
    const minSize = Math.round(Math.min(w, h) * lerp(0.40, 0.35, d));
    const maxSize = Math.round(Math.min(w, h) * lerp(0.65, 0.55, d));
    const placed = [];

    for(let i=0; i<targetCount; i++){
      let placedThis = false;
      for(let attempt=0; attempt<90; attempt++){
        const target = minSize + Math.random() * Math.max(1, (maxSize - minSize));
        const scale = target / Math.max(crop.width, crop.height);
        const dw = Math.max(8, Math.round(crop.width * scale));
        const dh = Math.max(8, Math.round(crop.height * scale));

        const x = Math.round(Math.random() * Math.max(0, w - dw));
        const y = Math.round(Math.random() * Math.max(0, h - dh));

        const margin = Math.round(lerp(8, 14, d));
        const rect = {x: x - margin, y: y - margin, w: dw + margin*2, h: dh + margin*2};
        if(hasRectOverlap(rect, placed)) continue;

        placed.push(rect);
        octx.drawImage(crop, 0, 0, crop.width, crop.height, x, y, dw, dh);
        placedThis = true;
        break;
      }
      if(!placedThis && placed.length < 2){
        return null;
      }
    }

    if(placed.length < 2) return null;
    const sig = `OBJ${placed.length}_${placed.map(r=>`${r.x}|${r.y}|${r.w}|${r.h}`).join(';')}`;
    return Object.assign(out, {_sig: sig});
  }

  function extractAlphaBounds(canvas, alphaThreshold=16){
    const w = canvas.width, h = canvas.height;
    const ctx = canvas.getContext('2d', {willReadFrequently:true});
    const data = ctx.getImageData(0, 0, w, h).data;
    let minX = w, minY = h, maxX = -1, maxY = -1;
    for(let y=0; y<h; y++){
      for(let x=0; x<w; x++){
        const a = data[(y*w + x)*4 + 3];
        if(a > alphaThreshold){
          if(x < minX) minX = x;
          if(y < minY) minY = y;
          if(x > maxX) maxX = x;
          if(y > maxY) maxY = y;
        }
      }
    }
    if(maxX < minX || maxY < minY) return null;
    return {x:minX, y:minY, w:maxX-minX+1, h:maxY-minY+1};
  }

  function hasRectOverlap(rect, rects){
    for(const r of rects){
      if(!(rect.x + rect.w <= r.x || r.x + r.w <= rect.x || rect.y + rect.h <= r.y || r.y + r.h <= rect.y)){
        return true;
      }
    }
    return false;
  }

  function avgColor(img){
    const s=32;
    const c=document.createElement('canvas'); c.width=s; c.height=s;
    const ctx=c.getContext('2d');
    ctx.drawImage(img,0,0,s,s);
    const data=ctx.getImageData(0,0,s,s).data;
    let r=0,g=0,b=0,n=0;
    for(let i=0;i<data.length;i+=4){
      r+=data[i]; g+=data[i+1]; b+=data[i+2]; n++;
    }
    return `rgb(${(r/n)|0},${(g/n)|0},${(b/n)|0})`;
  }
  function pick(arr){ return arr[(Math.random()*arr.length)|0]; }

  /* ================== Init ================== */
  SP.init = function(){
    SP.resetCaches();
    SP.config.enabled = true;
  };

  SP.evaluateVariantAdvanced = evaluateVariantAdvanced;
  global.SimilarityPipeline = SP;

})(typeof window!=='undefined'?window:global);