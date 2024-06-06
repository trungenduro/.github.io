//+------------------------------------------------------------------+
//|                                                     childEA4.mq4 |
//|                                  Copyright 2024, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property strict
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+

#import "shell32.dll"
int ShellExecuteW(int hWnd,int lpVerb,string lpFile,string lpParameters,string lpDirectory,int nCmdShow);  
#import 

int          positions;     
int child_positions;
 
void CheckPosition()
 {
  int curr_positions=OrdersTotal();
  
  //Print("Check pos positions=",positions, "  curr_positions ",curr_positions);
  if(curr_positions!=positions)
    {  
    PrintFormat("Number of positions has been changed. Previous value is %d, current value is %d",
                 positions,curr_positions);                  
     positions=curr_positions;     
     WriteParent();
    }    
 }
 
 void CheckChildPosition()
 {
  int childcurr_positions=ReadChild();
  if(childcurr_positions==-1) return;
  if(childcurr_positions!=child_positions)
    {  
         PrintFormat("Number of Parent position has been changed. Previous value is %d, current value is %d",
         child_positions,childcurr_positions); 
         ChildPositionChange(childcurr_positions);    
    }    
 }
 
 void ChildPositionChange(int newpos)
 {
   if( newpos==0 && child_positions>0){
      Print(" check check child 0 0 0000 ");
       Print(" ==== Close ALL ===  ");
       Print(" ==== Close ALL ===  ");
       Print(" ==== Close ALL ===  ");
      CloseAll();
   }  
   child_positions =  newpos;
 }
 
 

 string GetInfo(string info="MT4")
 {
  string varDate=TimeToString(__DATETIME__);
    StringReplace( varDate," ","_");
    string mt5a= info+ "_" + varDate + "_"+ IntegerToString(AccountInfoInteger(ACCOUNT_LOGIN));
  //  string mt5a=  info + "_" + IntegerToString(AccountInfoInteger(ACCOUNT_LOGIN));
     string mt5b=  IntegerToString(  (int)AccountInfoDouble(ACCOUNT_BALANCE));
   string mt5c= IntegerToString( (int) AccountInfoDouble(ACCOUNT_PROFIT));
    string mt5d= IntegerToString( (int) AccountInfoDouble(ACCOUNT_EQUITY));
 
   return mt5a + " " + mt5b + " " + mt5c + " " + mt5d;
 }
int OnInit()
  {
 
   Print("===== New MT ======================");
   Print("TERMINAL_COMMONDATA_PATH = ",TerminalInfoString(TERMINAL_COMMONDATA_PATH));
   positions=OrdersTotal();
   Print("TestEA4");
   child_positions =  ReadChild();
   Print("login = ",AccountInfoInteger(ACCOUNT_LOGIN)," BALANCE=",AccountInfoDouble(ACCOUNT_BALANCE));
    Print("GetInfonew = ",GetInfo());
   Print(" === init child_positions=",child_positions);
   Print(" === init positions=",positions);
   
   GetPosArray(CurrentPos);
    
   for(int i = 0; i < ArraySize(CurrentPos); i++)
   {
        
      Print("CurrentPos-i=",i," object tickket=",CurrentPos[i].ticket, "  ",CurrentPos[i].posSymBol, " ",CurrentPos[i].Type, " qty=",CurrentPos[i].QTY);
     
   }
   
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//---
   
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
   CheckPosition();
 //  CheckChildPosition();
   //Print("   Tick");
  }
//+------------------------------------------------------------------+
//| Trade function                                                   |
//+------------------------------------------------------------------+
void OnTrade()
  {
  
 // MessageBox("Traded");
//Print( " On trade ");
 CheckPosition();
 //CheckChildPosition();
  }
//+------------------------------------------------------------------+

class PosObject{

   public :
   PosObject(){
   }
     PosObject(string st)
    {
        string result[];               // An array to get strings
   
         ushort  u_sep=StringGetCharacter(",",0);
   
         int k=StringSplit(st,u_sep,result); 
         if (k>3)
         {
            ticket = StringToInteger( result[0]);
            QTY = StringToDouble(result[3]);
            posSymBol = result[1];
            posType = result[2];
         }
    
    }
    
   PosObject(int i){   
    
         OrderSelect(i, SELECT_BY_POS);      
      // OrderClose( OrderTicket(), OrderLots(), MarketInfo(OrderSymbol(), MODE_ASK), 5, Red );
         ulong ticketNum = OrderTicket();
     
         ticket = ticketNum;
         posSymBol = OrderSymbol();
         QTY =   OrderLots();
         posType = "Sell";
         int type   = OrderType();
          if(type == OP_BUY)
              {
                  posType = "Buy";
              }
             if(type == OP_SELL   )
              {
                  posType = "Sell";
              }    
      
   }
   
   string ToString()
   {
      return posType + " " + posSymBol ;
   }
   ulong ticket;
   string Type;
   string posSymBol;
   string posType;
   double QTY;
      string comment;
   bool isNew;
};
PosObject CurrentPos[];

  void GetPosArray(PosObject &t[])
  { 
      ArrayResize(t,0); 
      for(int i = 0; i < OrdersTotal(); i++)
      {
       
         ArrayResize(t,i +1 );   
          PosObject o(i);             
         t[i] = o;
      }
  }
//+------------------------------------------------------------------+

void CheckNewPosition(PosObject &parentPos[],PosObject &childPos[] )
{
   //find new order 
    for(int i = 0; i < ArraySize(parentPos); i++)
   {
      parentPos[i].isNew = true;
   }
   for(int i = 0; i < ArraySize(childPos); i++)
   {
       childPos[i].isNew = true;  
        for(int j= 0; j < ArraySize(parentPos); j++)
         {
            if(parentPos[j].comment== IntegerToString( childPos[i].ticket))
            {
               childPos[i].isNew = false;
               parentPos[j].isNew = false;
            }         
         }       
    }
      for(int i = 0; i < ArraySize(parentPos); i++)
      {
           if( parentPos[i].isNew )
           {
               ClosePos(parentPos[i]);
              // Print("Close pos ",parentPos[i].comment ," ",parentPos[i].ticket, " QTY=",parentPos[i].QTY );
           }
      }
        for(int i = 0; i < ArraySize(childPos); i++)
      {
           if( childPos[i].isNew )
           {
               AddNewPos(childPos[i]);
           }
      }
} 

void AddNewPos(PosObject &ob)
{
       Print("===== New Child Order =", ob.ticket, " Symbol", ob.posSymBol, " ",ob.posType, " Qty", ob.QTY);
 
   if(ob.posType=="Buy"){
    //  Trade.Buy(ob.posSymBol, ob.QTY,  0,  0, ob.ticket);
      Print("Trade.Buy(",ob.posSymBol,",", ob.QTY,",", ob.ticket);
   }
     if(ob.posType=="Sell"){
  // Trade.Sell(ob.posSymBol, ob.QTY,  0,  0, ob.ticket);
    Print("Trade.Sell(",ob.posSymBol,",", ob.QTY,",", ob.ticket);
   } 
}

void ClosePos(PosObject &ob)
{
   if(_Symbol!= ob.posSymBol){  
       Print("==khac",_Symbol , "!=", ob.posSymBol );
    return;
    }
       Print("===== close Child Order =", ob.ticket, " Symbol", ob.posSymBol, " ",ob.posType, " Qty", ob.QTY); 
    //  Trade.ClosePosition(ob.ticket, ob.QTY);     
}


void WriteParent()
{

 int h=FileOpen("child.txt",FILE_WRITE|FILE_ANSI|FILE_TXT);
   if(h==INVALID_HANDLE){
      Print("Error opening file");
      return;
   }
   for(int i = 0; i < OrdersTotal(); i++)
   {
    OrderSelect(i, SELECT_BY_POS);
      PosObject o(i);
      //FileWrite(h,TimeToStr( TimeCurrent()) + ","+ o.posSymBol + "," + o.posType); 
      FileWrite(h,o.ticket + ","+ o.posSymBol + "," + o.posType + "," + DoubleToString(o.QTY) );   
   }
   
   FileClose(h);
    string parentPath= TerminalInfoString(TERMINAL_DATA_PATH) + "\\MQL4\Files";
   ShellExecuteW(NULL,"open",TerminalInfoString(TERMINAL_COMMONDATA_PATH) + "\\CopyMT.exe",parentPath,NULL,1);
  // ShellExecuteW(NULL,"open",TerminalInfoString(TERMINAL_COMMONDATA_PATH) + "\\CopyMT4_5.bat",NULL,NULL,1);
  //ShellExecuteW(NULL,"open",TerminalInfoString(TERMINAL_COMMONDATA_PATH) + "\\CopyMT.exe",GetInfo("MT4_change"),NULL,1);
   Print("Write file ok ",GetInfo());
   Print("Write file ok");

}

int ReadChild()
{

string table[];
   
   int i=0;
  
   int fileHandle = FileOpen("parent.txt",FILE_READ|FILE_ANSI|FILE_TXT);
     if(fileHandle==INVALID_HANDLE) {
         Print("cannnot read");
     
      return -1;}
   if(fileHandle!=INVALID_HANDLE) 
    {
     while(FileIsEnding(fileHandle) == false)
       {    
        ArrayResize(table,ArraySize(table) +1 );     
        table[ArraySize(table)-1] = FileReadString(fileHandle);
      //   Print(i," read parent lines number=",table[i] );
       i++;      
      }
    
     FileClose(fileHandle);          
    }
    
     //Print(" Read child=",ArraySize(table) );
  //  Print("  child position number =",ArraySize(table) );
    return ArraySize(table);
    //Print("file lines number=",ArraySize(table) );
}


int CloseAll()
{
return -1;
  int total = OrdersTotal();
  for(int i=total-1;i>=0;i--)
  {
    OrderSelect(i, SELECT_BY_POS);
    int type   = OrderType();

    bool result = false;
    
    switch(type)
    {
      //Close opened long positions
      case OP_BUY       : result = OrderClose( OrderTicket(), OrderLots(), MarketInfo(OrderSymbol(), MODE_BID), 5, Red );
                          break;
      
      //Close opened short positions
      case OP_SELL      : result = OrderClose( OrderTicket(), OrderLots(), MarketInfo(OrderSymbol(), MODE_ASK), 5, Red );
                          break;

      //Close pending orders
      case OP_BUYLIMIT  :
      case OP_BUYSTOP   :
      case OP_SELLLIMIT :
      case OP_SELLSTOP  : result = OrderDelete( OrderTicket() );
    }
    
    if(result == false)
    {
      Alert("Order " , OrderTicket() , " failed to close. Error:" , GetLastError() );
      Sleep(3000);
    }  
  }
  //  ShellExecuteW(NULL,"open",TerminalInfoString(TERMINAL_COMMONDATA_PATH) + "\\CopyMT.exe",GetInfo("MT4_Close"),NULL,1);
   Print("Close ALL  ",GetInfo());
  return(0);
}


string CheckHttp( string url1="Getdata?title=05")
  {
  //https://trung1081.bsite.net/Comments/setdata?title=06&content1=0601
   string cookie=NULL,headers;
   char   post[],result[];
   string url= "https://trung1081.bsite.net/Comments/" + url1;

   ResetLastError();
//--- Downloading a html page from Yahoo Finance
   int res=WebRequest("GET",url,cookie,NULL,500,post,0,result,headers);
   if(res==-1)
     {
     return "-1";
      Print("Error in WebRequest. Error code  =",GetLastError());
     }
   else
     {
      if(res==200)
        {         
         
         Print("The file has been successfully downloaded, File size=",CharArrayToString(result));
         return CharArrayToString(result);
        }
      else
         PrintFormat("Downloading '%s' failed, error code %d",url,res);
         
        return "-1";
     }
  }