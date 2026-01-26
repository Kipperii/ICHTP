stop();
game_success = 0;
game_fail = 0;
if(_root.CurrentGameLevel < 4)
{
   var set_result_lv = new LoadVars();
   set_result_lv.onLoad = function(success)
   {
      if(success)
      {
         if(_root.GamePlay == true)
         {
            _root.BackFromGame(true);
         }
         else
         {
            stop();
         }
      }
      else
      {
         stop();
      }
   };
   var set_result_send_lv = new LoadVars();
   set_result_send_lv.session_no = "1";
   set_result_send_lv.game_type = "1";
   set_result_send_lv.game_stage = _root.CurrentGameLevel;
   set_result_send_lv.game_no = _root.CurrentGameNo;
   set_result_send_lv.game_level1 = 1;
   set_result_send_lv.game_trail1 = 1;
   set_result_send_lv.try01_ans1 = result_ans[0][0][0];
   set_result_send_lv.try01_time1 = result_time[0][0][0];
   set_result_send_lv.try01_success1 = result_success[0][0][0];
   set_result_send_lv.try02_ans1 = result_ans[0][0][1];
   set_result_send_lv.try02_time1 = result_time[0][0][1];
   set_result_send_lv.try02_success1 = result_success[0][0][1];
   if(result_success[0][0][0] == "Y" || result_success[0][0][1] == "Y")
   {
      game_success++;
   }
   else
   {
      game_fail++;
   }
   set_result_send_lv.game_level2 = 1;
   set_result_send_lv.game_trail2 = 2;
   set_result_send_lv.try01_ans2 = result_ans[0][1][0];
   set_result_send_lv.try01_time2 = result_time[0][1][0];
   set_result_send_lv.try01_success2 = result_success[0][1][0];
   set_result_send_lv.try02_ans2 = result_ans[0][1][1];
   set_result_send_lv.try02_time2 = result_time[0][1][1];
   set_result_send_lv.try02_success2 = result_success[0][1][1];
   if(result_success[0][1][0] == "Y" || result_success[0][1][1] == "Y")
   {
      game_success++;
   }
   else
   {
      game_fail++;
   }
   set_result_send_lv.game_level3 = 1;
   set_result_send_lv.game_trail3 = 3;
   set_result_send_lv.try01_ans3 = result_ans[0][2][0];
   set_result_send_lv.try01_time3 = result_time[0][2][0];
   set_result_send_lv.try01_success3 = result_success[0][2][0];
   set_result_send_lv.try02_ans3 = result_ans[0][2][1];
   set_result_send_lv.try02_time3 = result_time[0][2][1];
   set_result_send_lv.try02_success3 = result_success[0][2][1];
   if(result_success[0][2][0] == "Y" || result_success[0][2][1] == "Y")
   {
      game_success++;
   }
   else
   {
      game_fail++;
   }
   set_result_send_lv.game_level4 = 1;
   set_result_send_lv.game_trail4 = 4;
   set_result_send_lv.try01_ans4 = result_ans[0][3][0];
   set_result_send_lv.try01_time4 = result_time[0][3][0];
   set_result_send_lv.try01_success4 = result_success[0][3][0];
   set_result_send_lv.try02_ans4 = result_ans[0][3][1];
   set_result_send_lv.try02_time4 = result_time[0][3][1];
   set_result_send_lv.try02_success4 = result_success[0][3][1];
   if(result_success[0][3][0] == "Y" || result_success[0][3][1] == "Y")
   {
      game_success++;
   }
   else
   {
      game_fail++;
   }
   set_result_send_lv.game_level5 = 1;
   set_result_send_lv.game_trail5 = 5;
   set_result_send_lv.try01_ans5 = result_ans[0][4][0];
   set_result_send_lv.try01_time5 = result_time[0][4][0];
   set_result_send_lv.try01_success5 = result_success[0][4][0];
   set_result_send_lv.try02_ans5 = result_ans[0][4][1];
   set_result_send_lv.try02_time5 = result_time[0][4][1];
   set_result_send_lv.try02_success5 = result_success[0][4][1];
   if(result_success[0][4][0] == "Y" || result_success[0][4][1] == "Y")
   {
      game_success++;
   }
   else
   {
      game_fail++;
   }
   set_result_send_lv.game_level6 = 2;
   set_result_send_lv.game_trail6 = 1;
   set_result_send_lv.try01_ans6 = result_ans[1][0][0];
   set_result_send_lv.try01_time6 = result_time[1][0][0];
   set_result_send_lv.try01_success6 = result_success[1][0][0];
   set_result_send_lv.try02_ans6 = result_ans[1][0][1];
   set_result_send_lv.try02_time6 = result_time[1][0][1];
   set_result_send_lv.try02_success6 = result_success[1][0][1];
   if(result_success[1][0][0] == "Y" || result_success[1][0][1] == "Y")
   {
      game_success++;
   }
   else
   {
      game_fail++;
   }
   set_result_send_lv.game_level7 = 2;
   set_result_send_lv.game_trail7 = 2;
   set_result_send_lv.try01_ans7 = result_ans[1][1][0];
   set_result_send_lv.try01_time7 = result_time[1][1][0];
   set_result_send_lv.try01_success7 = result_success[1][1][0];
   set_result_send_lv.try02_ans7 = result_ans[1][1][1];
   set_result_send_lv.try02_time7 = result_time[1][1][1];
   set_result_send_lv.try02_success7 = result_success[1][1][1];
   if(result_success[1][1][0] == "Y" || result_success[1][1][1] == "Y")
   {
      game_success++;
   }
   else
   {
      game_fail++;
   }
   set_result_send_lv.game_level8 = 2;
   set_result_send_lv.game_trail8 = 3;
   set_result_send_lv.try01_ans8 = result_ans[1][2][0];
   set_result_send_lv.try01_time8 = result_time[1][2][0];
   set_result_send_lv.try01_success8 = result_success[1][2][0];
   set_result_send_lv.try02_ans8 = result_ans[1][2][1];
   set_result_send_lv.try02_time8 = result_time[1][2][1];
   set_result_send_lv.try02_success8 = result_success[1][2][1];
   if(result_success[1][2][0] == "Y" || result_success[1][2][1] == "Y")
   {
      game_success++;
   }
   else
   {
      game_fail++;
   }
   set_result_send_lv.game_level9 = 2;
   set_result_send_lv.game_trail9 = 4;
   set_result_send_lv.try01_ans9 = result_ans[1][3][0];
   set_result_send_lv.try01_time9 = result_time[1][3][0];
   set_result_send_lv.try01_success9 = result_success[1][3][0];
   set_result_send_lv.try02_ans9 = result_ans[1][3][1];
   set_result_send_lv.try02_time9 = result_time[1][3][1];
   set_result_send_lv.try02_success9 = result_success[1][3][1];
   if(result_success[1][3][0] == "Y" || result_success[1][3][1] == "Y")
   {
      game_success++;
   }
   else
   {
      game_fail++;
   }
   set_result_send_lv.game_level10 = 2;
   set_result_send_lv.game_trail10 = 5;
   set_result_send_lv.try01_ans10 = result_ans[1][4][0];
   set_result_send_lv.try01_time10 = result_time[1][4][0];
   set_result_send_lv.try01_success10 = result_success[1][4][0];
   set_result_send_lv.try02_ans10 = result_ans[1][4][1];
   set_result_send_lv.try02_time10 = result_time[1][4][1];
   set_result_send_lv.try02_success10 = result_success[1][4][1];
   if(result_success[1][4][0] == "Y" || result_success[1][4][1] == "Y")
   {
      game_success++;
   }
   else
   {
      game_fail++;
   }
   set_result_send_lv.game_level11 = 3;
   set_result_send_lv.game_trail11 = 1;
   set_result_send_lv.try01_ans11 = result_ans[2][0][0];
   set_result_send_lv.try01_time11 = result_time[2][0][0];
   set_result_send_lv.try01_success11 = result_success[2][0][0];
   set_result_send_lv.try02_ans11 = result_ans[2][0][1];
   set_result_send_lv.try02_time11 = result_time[2][0][1];
   set_result_send_lv.try02_success11 = result_success[2][0][1];
   if(result_success[2][0][0] == "Y" || result_success[2][0][1] == "Y")
   {
      game_success++;
   }
   else
   {
      game_fail++;
   }
   set_result_send_lv.game_level12 = 3;
   set_result_send_lv.game_trail12 = 2;
   set_result_send_lv.try01_ans12 = result_ans[2][1][0];
   set_result_send_lv.try01_time12 = result_time[2][1][0];
   set_result_send_lv.try01_success12 = result_success[2][1][0];
   set_result_send_lv.try02_ans12 = result_ans[2][1][1];
   set_result_send_lv.try02_time12 = result_time[2][1][1];
   set_result_send_lv.try02_success12 = result_success[2][1][1];
   if(result_success[2][1][0] == "Y" || result_success[2][1][1] == "Y")
   {
      game_success++;
   }
   else
   {
      game_fail++;
   }
   set_result_send_lv.game_level13 = 3;
   set_result_send_lv.game_trail13 = 3;
   set_result_send_lv.try01_ans13 = result_ans[2][2][0];
   set_result_send_lv.try01_time13 = result_time[2][2][0];
   set_result_send_lv.try01_success13 = result_success[2][2][0];
   set_result_send_lv.try02_ans13 = result_ans[2][2][1];
   set_result_send_lv.try02_time13 = result_time[2][2][1];
   set_result_send_lv.try02_success13 = result_success[2][2][1];
   if(result_success[2][2][0] == "Y" || result_success[2][2][1] == "Y")
   {
      game_success++;
   }
   else
   {
      game_fail++;
   }
   set_result_send_lv.game_level14 = 3;
   set_result_send_lv.game_trail14 = 4;
   set_result_send_lv.try01_ans14 = result_ans[2][3][0];
   set_result_send_lv.try01_time14 = result_time[2][3][0];
   set_result_send_lv.try01_success14 = result_success[2][3][0];
   set_result_send_lv.try02_ans14 = result_ans[2][3][1];
   set_result_send_lv.try02_time14 = result_time[2][3][1];
   set_result_send_lv.try02_success14 = result_success[2][3][1];
   if(result_success[2][3][0] == "Y" || result_success[2][3][1] == "Y")
   {
      game_success++;
   }
   else
   {
      game_fail++;
   }
   set_result_send_lv.game_level15 = 3;
   set_result_send_lv.game_trail15 = 5;
   set_result_send_lv.try01_ans15 = result_ans[2][4][0];
   set_result_send_lv.try01_time15 = result_time[2][4][0];
   set_result_send_lv.try01_success15 = result_success[2][4][0];
   set_result_send_lv.try02_ans15 = result_ans[2][4][1];
   set_result_send_lv.try02_time15 = result_time[2][4][1];
   set_result_send_lv.try02_success15 = result_success[2][4][1];
   if(result_success[2][4][0] == "Y" || result_success[2][4][1] == "Y")
   {
      game_success++;
   }
   else
   {
      game_fail++;
   }
   _root.game1_1_success = game_success;
   _root.game1_1_fail = game_fail;
   set_result_send_lv.sendAndLoad("SetGameResult1.asp",set_result_lv,"POST");
}
else if(_root.GamePlay == true)
{
   _root.BackFromGame(true);
}
else
{
   stop();
}
