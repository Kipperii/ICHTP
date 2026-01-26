s1 = new Sound(this);
s1.attachSound("Sound_Time");
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
