
### try 

是的，C#中有類似Python的try-catch結構，用於處理異常（exceptions）。以下是一個簡單的例子：

```csharp
using System;

class Program
{
    static void Main()
    {
        try
        {
            // 這裡放置可能引發異常的程式碼
            int numerator = 10;
            int denominator = 0;
            int result = numerator / denominator; // 這裡會引發 DivideByZeroException
            Console.WriteLine(result); // 不會執行到這裡
        }
        catch (DivideByZeroException ex)
        {
            // 異常處理代碼
            Console.WriteLine("Error: " + ex.Message);
        }
        finally
        {
            // finally 區塊中的程式碼無論是否有異常都會執行
            Console.WriteLine("Finally block");
        }

        // 繼續執行的程式碼
        Console.WriteLine("Program continues...");
    }
}
```

在上述例子中，try區塊包含可能引發異常的程式碼，catch區塊用於處理特定類型的異常（DivideByZeroException），而finally區塊中的程式碼則無論是否有異常都會執行。