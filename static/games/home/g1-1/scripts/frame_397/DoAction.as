time_count++;
if(time_count > 60)
{
   result_ans[current_level - 1][current_no - 1][retry_count] = "0";
   result_success[current_level - 1][current_no - 1][retry_count] = "N";
   result_time[current_level - 1][current_no - 1][retry_count] = time_count;
   if(retry_count == 0)
   {
      retry_count = 1;
      gotoAndStop("LevelTimeoutReplay");
      play();
   }
   else
   {
      gotoAndStop("LevelTimeoutFail");
      play();
   }
}
else
{
   gotoAndPlay(_currentframe - 11);
}
