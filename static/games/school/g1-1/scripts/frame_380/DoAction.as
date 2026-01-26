var tempQ = current_level + "_" + current_no + "_";
Question.loadMovie(gamePath + tempQ + "Q.jpg","POST");
time_count = 0;
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
