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
