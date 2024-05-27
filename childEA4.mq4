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
    string mt5a=  info + "_" + IntegerToString(AccountInfoInteger(ACCOUNT_LOGIN));
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
    
   Print(" === init child_positions=",child_positions);
   Print(" === init positions=",positions);
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
   CheckChildPosition();
   //Print("   Tick");
  }
//+------------------------------------------------------------------+
//| Trade function                                                   |
//+------------------------------------------------------------------+
void OnTrade()
  {
  
  MessageBox("Traded");
Print( " On trade ");
 CheckPosition();
 CheckChildPosition();
  }
//+------------------------------------------------------------------+

class PosObject{

public :
PosObject(int i){

   if (i < OrdersTotal())
   {
    
  //  bool check=  OrderSelect( i, SELECT_BY_POS, MODE_TRADES ); 
      posSymBol="BTC";
      posType = "Sell";
   }
}

string ToString()
{
   return posType + " " + posSymBol;
}
ulong ticket;
string Type;
string posSymBol;
string posType;
};


//+------------------------------------------------------------------+

void WriteParent()
{

 int h=FileOpen("child.txt",FILE_WRITE|FILE_ANSI|FILE_TXT);
   if(h==INVALID_HANDLE){
      Print("Error opening file");
      return;
   }
   for(int i = 0; i < OrdersTotal(); i++)
   {
      PosObject o(i);
      FileWrite(h,TimeToStr( TimeCurrent()) + ","+ o.posSymBol + "," + o.posType); 
   }
   
   FileClose(h);
    string parentPath= TerminalInfoString(TERMINAL_DATA_PATH) + "\\MQL4\Files";
   ShellExecuteW(NULL,"open",TerminalInfoString(TERMINAL_COMMONDATA_PATH) + "\\CopyMT.exe",parentPath,NULL,1);
  // ShellExecuteW(NULL,"open",TerminalInfoString(TERMINAL_COMMONDATA_PATH) + "\\CopyMT4_5.bat",NULL,NULL,1);
  ShellExecuteW(NULL,"open",TerminalInfoString(TERMINAL_COMMONDATA_PATH) + "\\CopyMT.exe",GetInfo("MT4_change"),NULL,1);
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
    ShellExecuteW(NULL,"open",TerminalInfoString(TERMINAL_COMMONDATA_PATH) + "\\CopyMT.exe",GetInfo("MT4_Close"),NULL,1);
   Print("Close ALL  ",GetInfo());
  return(0);
}