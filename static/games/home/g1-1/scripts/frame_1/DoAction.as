stop();
onEnterFrame = function()
{
   LB = getBytesLoaded();
   TB = getBytesTotal();
   PC = LB / TB * 100;
   loaderbar.setbar(PC);
   if(TB > 4 && PC == 100)
   {
      delete onEnterFrame;
      gotoAndStop("loadinitialize");
      play();
   }
};
