var gamePath = "Game1-1/";
var i;
var j;
var k;
var s1;
var canPress = false;
var retry_count = 0;
var time_count = 0;
var current_level = 1;
var current_no = 1;
var ans_y = 492.1;
var ans1_x = 49.4;
var ans2_x = 293.4;
var ans3_x = 541.5;
var ans4_x = 783.5;
var ans = new Array(3);
i = 0;
while(i < 3)
{
   ans[i] = new Array(5);
   i++;
}
ans[0][0] = 1;
ans[0][1] = 4;
ans[0][2] = 2;
ans[0][3] = 4;
ans[0][4] = 3;
ans[1][0] = 3;
ans[1][1] = 1;
ans[1][2] = 1;
ans[1][3] = 4;
ans[1][4] = 3;
ans[2][0] = 4;
ans[2][1] = 4;
ans[2][2] = 4;
ans[2][3] = 1;
ans[2][4] = 4;
var result_ans = new Array(3);
var result_time = new Array(3);
var result_success = new Array(3);
i = 0;
while(i < 3)
{
   result_ans[i] = new Array(5);
   result_time[i] = new Array(5);
   result_success[i] = new Array(5);
   j = 0;
   while(j < 5)
   {
      result_ans[i][j] = new Array(2);
      result_time[i][j] = new Array(2);
      result_success[i][j] = new Array(2);
      j++;
   }
   i++;
}
i = 0;
while(i < 3)
{
   j = 0;
   while(j < 5)
   {
      k = 0;
      while(k < 2)
      {
         result_ans[i][j][k] = 0;
         result_time[i][j][k] = 0;
         result_success[i][j][k] = "";
         k++;
      }
      j++;
   }
   i++;
}
