function setbar(PC)
{
   if(PC <= 50)
   {
      s2.mask._rotation = 0;
      s1.mask._rotation = 180 * (PC / 50);
   }
   else
   {
      s1.mask._rotation = 180;
      s2.mask._rotation = 180 * ((PC - 50) / 50);
   }
}
