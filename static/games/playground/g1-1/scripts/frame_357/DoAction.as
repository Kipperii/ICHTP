Life1._visible = true;
Life2._visible = true;
time_count = 0;
PowerBar.TimeWord._visible = false;
PowerBar.yellow._width = 247 * time_count / 60;
PowerBar.red._width = 247 * time_count / 60;
PowerBar.green._width = 247 * time_count / 60;
if(time_count < 30)
{
   PowerBar.TimeWord._visible = false;
   PowerBar.yellow._visible = false;
   PowerBar.red._visible = false;
   PowerBar.green._visible = true;
}
else if(time_count < 50)
{
   PowerBar.TimeWord._visible = false;
   PowerBar.yellow._visible = true;
   PowerBar.red._visible = false;
   PowerBar.green._visible = false;
}
else
{
   PowerBar.TimeWord._visible = true;
   PowerBar.yellow._visible = false;
   PowerBar.red._visible = true;
   PowerBar.green._visible = false;
}
if(current_level == 1)
{
   mcLv1._visible = true;
   mcLv2._visible = false;
   mcLv3._visible = false;
   GameStartLevel1._visible = true;
   GameStartLevel2._visible = false;
   GameStartLevel3._visible = false;
}
if(current_level == 2)
{
   mcLv1._visible = false;
   mcLv2._visible = true;
   mcLv3._visible = false;
   GameStartLevel1._visible = false;
   GameStartLevel2._visible = true;
   GameStartLevel3._visible = false;
}
if(current_level == 3)
{
   mcLv1._visible = false;
   mcLv2._visible = false;
   mcLv3._visible = true;
   GameStartLevel1._visible = false;
   GameStartLevel2._visible = false;
   GameStartLevel3._visible = true;
}
