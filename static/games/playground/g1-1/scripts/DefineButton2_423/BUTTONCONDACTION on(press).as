on(press){
   s1.stop("Sound_Replay");
   s1.stop("Sound_Fail");
   s1.stop("Sound_Time");
   s1.stop("Sound_Time_Next");
   s1.stop("Sound_Win1");
   s1.stop("Sound_Win2");
   s1.stop("Sound_Win3");
   current_no++;
   if(current_no > 5)
   {
      current_level++;
      current_no = 1;
   }
   if(current_level <= 3)
   {
      retry_count = 0;
      if(current_no == 1)
      {
         gotoAndStop("GameStart");
         play();
      }
      else
      {
         gotoAndStop("LevelStart");
         play();
      }
   }
   else
   {
      gotoAndStop("StageComplete");
      play();
   }
}
