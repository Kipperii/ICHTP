import glob

for filepath in glob.glob("app/templates/games/**/g1-2/*.html", recursive=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = content.replace('this.timerText.setText(${TEXTS.time}: );', 'this.timerText.setText(`${TEXTS.time}: ${this.timeLeft}`);')
    new_content = new_content.replace('this.timerText=this.add.text(GAME_W-SAFE-380,SAFE+0,${TEXTS.time}: ,{font', 'this.timerText=this.add.text(GAME_W-SAFE-380,SAFE+0,`${TEXTS.time}: ${this.timeLeft}`,{font')
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")
