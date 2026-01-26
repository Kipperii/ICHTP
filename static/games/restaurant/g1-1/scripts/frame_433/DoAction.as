tempnum = Math.ceil(Math.random() * 3);
s1 = new Sound(this);
if(current_level == 3 && current_no == 5)
{
   s1.attachSound("Sound_Win_GameOver");
   btnWin._visible = false;
   btnWinGameOver._visible = true;
}
else
{
   s1.attachSound("Sound_Win" + tempnum);
   btnWin._visible = true;
   btnWinGameOver._visible = false;
}
s1.start();
if(retry_count == 0)
{
   Life1._visible = true;
   Life2._visible = true;
}
else if(retry_count == 1)
{
   Life1._visible = true;
   Life2._visible = false;
}
else
{
   Life1._visible = false;
   Life2._visible = false;
}
ChoiceA_btn._visible = false;
ChoiceB_btn._visible = false;
ChoiceC_btn._visible = false;
ChoiceD_btn._visible = false;
ChoiceA._alpha = 30;
ChoiceB._alpha = 30;
ChoiceC._alpha = 30;
ChoiceD._alpha = 30;
var tempstr = current_level + "_" + current_no + "_";
if(ans[current_level - 1][current_no - 1] == 1)
{
   ChoiceA.loadMovie(gamePath + tempstr + "ans.jpg","POST");
   ChoiceA._alpha = 100;
   CorrectAnswer._x = 63;
}
if(ans[current_level - 1][current_no - 1] == 2)
{
   ChoiceB.loadMovie(gamePath + tempstr + "ans.jpg","POST");
   ChoiceB._alpha = 100;
   CorrectAnswer._x = 305.9;
}
if(ans[current_level - 1][current_no - 1] == 3)
{
   ChoiceC.loadMovie(gamePath + tempstr + "ans.jpg","POST");
   ChoiceC._alpha = 100;
   CorrectAnswer._x = 558;
}
if(ans[current_level - 1][current_no - 1] == 4)
{
   ChoiceD.loadMovie(gamePath + tempstr + "ans.jpg","POST");
   ChoiceD._alpha = 100;
   CorrectAnswer._x = 800;
}
