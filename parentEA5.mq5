//+------------------------------------------------------------------+
//|                                                      TestEA1.mq5 |
//|                                  Copyright 2024, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"

#include <OriginalTrade.mqh>
#include <Math\Stat\Math.mqh>
input int SL=10000;//ストップロス
input int TP=30000;//テイクプロフィット
#include <Trade\Trade.mqh>
  #include <Files\FileTxt.mqh>
input int Deviation=50;//スリッページ  
  
#import "shell32.dll"
int ShellExecuteW(int hWnd,int lpVerb,string lpFile,string lpParameters,string lpDirectory,int nCmdShow);  
#import 

int          positions;     
int child_positions;
OriginalCTrade Trade;

 
void CheckPosition()
 {
  int curr_positions=PositionsTotal();
  
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
  if (childcurr_positions==-1) return;
  
  if(childcurr_positions!=child_positions)
    {  
         PrintFormat("Number of child position has been changed. Previous value is %d, current value is %d",
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
 
 
 string GetInfo(string info="MT5")
 {
    string mt5a= info+ "_" + IntegerToString(AccountInfoInteger(ACCOUNT_LOGIN));
     string mt5b=  IntegerToString(  (int)AccountInfoDouble(ACCOUNT_BALANCE));
   string mt5c= IntegerToString( (int) AccountInfoDouble(ACCOUNT_PROFIT));
    string mt5d= IntegerToString( (int) AccountInfoDouble(ACCOUNT_EQUITY));
 
   return mt5a + " " + mt5b + " " + mt5c + " " + mt5d;
 }
 
int OnInit()
  {
   Print("===== New MT ======================");
  Print("TERMINAL_PATH = ",TerminalInfoString(TERMINAL_PATH));
   Print("TERMINAL_DATA_PATH = ",TerminalInfoString(TERMINAL_DATA_PATH));
   Print("TERMINAL_COMMONDATA_PATH = ",TerminalInfoString(TERMINAL_COMMONDATA_PATH));
  
   Print("GetInfo = ",GetInfo());
   //Print("mt5c new = ",mt5a + " " + mt5b + " " + mt5c + " " + mt5c );
   string parentPath = TerminalInfoString(TERMINAL_DATA_PATH) + "\\MQL5\\Files";
  WritePath();
   
  ENUM_ORDER_TYPE_FILLING filltype=FillPolicy();
   Trade.SetDeviation(Deviation);
   Trade.SetFillType(filltype);
   
   positions=PositionsTotal();
   Print("TestEA5");
   child_positions =  ReadChild();
   int k = PositionsTotal();   
   
   for(int i = 0; i < PositionsTotal(); i++)
   {
       PosObject o(i);      
      Print("i=",i," object tickket=",o.ticket, "  ",o.posSymBol, " ",o.Type);
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
   CheckChildPosition();
  }
//+------------------------------------------------------------------+
//| Trade function                                                   |
//+------------------------------------------------------------------+
void OnTrade()
  {

 CheckPosition();
 CheckChildPosition();
  }
//+------------------------------------------------------------------+

class PosObject{

public :
PosObject(int i){

   if (i < PositionsTotal())
   {
      ulong ticketNum = PositionGetTicket(i);
      PositionSelectByTicket(ticketNum);  
      posSymBol = PositionGetSymbol(i);
      posType = "Sell";
       if(PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY)
           {
               posType = "Buy";
           }
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
void WritePath()
{
string parentPath= TerminalInfoString(TERMINAL_DATA_PATH) + "\\MQL5\Files\\parentPath.txt";
 int h=FileOpen("parentPath.txt",FILE_WRITE|FILE_ANSI|FILE_TXT);
   if(h==INVALID_HANDLE){
      Print("Error opening file");
      return;
   }
   FileWrite(h,parentPath);       
   FileClose(h);
  // C:\Users\user\AppData\Roaming\MetaQuotes\Terminal
  
 //  ShellExecuteW(NULL,"open",TerminalInfoString(TERMINAL_COMMONDATA_PATH) + "\\MT5.bat",parentPath,NULL,1);
//   Print("Write file path ok");

}

void WriteParent()
{

 int h=FileOpen("parent.txt",FILE_WRITE|FILE_ANSI|FILE_TXT);
   if(h==INVALID_HANDLE){
      Print("Error opening file");
      return;
   }
   for(int i = 0; i < PositionsTotal(); i++)
   {
      PosObject o(i);
      FileWrite(h,TimeCurrent() + ","+ o.posSymBol + "," + o.posType); 
   }
      
   FileClose(h);
  // C:\Users\user\AppData\Roaming\MetaQuotes\Terminal
  string parentPath= TerminalInfoString(TERMINAL_DATA_PATH) + "\\MQL5\Files";
   ShellExecuteW(NULL,"open",TerminalInfoString(TERMINAL_COMMONDATA_PATH) + "\\CopyMT.exe",parentPath,NULL,1);
   Print("Write file ok");
   
    ShellExecuteW(NULL,"open",TerminalInfoString(TERMINAL_COMMONDATA_PATH) + "\\CopyMT.exe",GetInfo("MT5_Change"),NULL,1);
   Print("Write file ok ",GetInfo());

}



int ReadChild()
{

string table[];
   
   int i=0;
   
   int fileHandle = FileOpen("child.txt",FILE_READ|FILE_ANSI|FILE_TXT);
   if(fileHandle==INVALID_HANDLE) return -1;
   if(fileHandle!=INVALID_HANDLE) 
    {
     while(FileIsEnding(fileHandle) == false)
       {    
        ArrayResize(table,ArraySize(table) +1 );     
        table[ArraySize(table)-1] = FileReadString(fileHandle);
      // Print(i,"  lines number=",table[i] );
       i++;      
      }
     FileClose(fileHandle);          
    }
  // Print("  child position number =",ArraySize(table) );
    return ArraySize(table);
    //Print("file lines number=",ArraySize(table) );
}


void CloseAll(){

  MqlTradeRequest request;
   MqlTradeResult result;

//構造体の初期化
   ZeroMemory(request);
   for(int i = 0; i < PositionsTotal(); i++)
     {
      ulong ticketNum = PositionGetTicket(i);
      PositionSelectByTicket(ticketNum);

      if(PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY)
        {
           request.action = TRADE_ACTION_DEAL;
         request.type = ORDER_TYPE_SELL;
         request.symbol = _Symbol;
         request.position = ticketNum;
         request.volume = PositionGetDouble(POSITION_VOLUME);
         request.price = SymbolInfoDouble(_Symbol,SYMBOL_BID);
         request.deviation = Deviation;
       

        }//if(PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY)

      else
         if(PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_SELL)
           {
             request.action = TRADE_ACTION_DEAL;
            request.type = ORDER_TYPE_BUY;
            request.symbol = _Symbol;
            request.position = ticketNum;
            request.volume = PositionGetDouble(POSITION_VOLUME);
            request.price = SymbolInfoDouble(_Symbol,SYMBOL_ASK);
            request.deviation = Deviation;

           }// else if(PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_SELL)

            bool sent = OrderSend(request, result);
     }//for(int i = 0; i < PositionsTotal(); i++)
 ShellExecuteW(NULL,"open",TerminalInfoString(TERMINAL_COMMONDATA_PATH) + "\\CopyMT.exe",GetInfo("MT5_Close"),NULL,1);
   Print("Close ALL  ",GetInfo());
  
}