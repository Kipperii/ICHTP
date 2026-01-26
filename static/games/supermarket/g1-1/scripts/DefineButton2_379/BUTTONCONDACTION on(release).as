on(release){
   if(ans[current_level - 1][current_no - 1] == 2)
   {
      result_ans[current_level - 1][current_no - 1][retry_count] = "2";
      result_success[current_level - 1][current_no - 1][retry_count] = "Y";
      result_time[current_level - 1][current_no - 1][retry_count] = time_count;
      gotoAndStop("LevelWin");
      play();
   }
   else
   {
      result_ans[current_level - 1][current_no - 1][retry_count] = "2";
      result_success[current_level - 1][current_no - 1][retry_count] = "N";
      result_time[current_level - 1][current_no - 1][retry_count] = time_count;
      if(retry_count == 0)
      {
         retry_count = 1;
         gotoAndStop("LevelReplay");
         play();
      }
      else
      {
         gotoAndStop("LevelFail");
         play();
      }
   }
}
