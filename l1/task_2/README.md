# L1 - 2019

## Task 2
Proof that you can use Vim:
- find an expression
  ```text
  Answer: Żeby zacząć wyszukiwanie należy wybrać "/".Wyszukanie konkretnego wzorca np. "i" odbywa się poprzez \<i\> .Podanie samego "i" skutkowało by wyszukaniem wszystkich wystąpień litery i - również w innych słowach."i" możemy zastąpić czymkolwiek, słowem lub całym wyrażeniem. Jeśli w wyrażeniu znajduje się np. nowa linia trzeba pamiętać o użyciu \n itp. 
    ```
- jump to line
  ```text
  Answer: ESC -> numer linii -> ENTER lub ESC -> numer linii -> SHIFT + G
  ```
- substitute a single character
  ```text
  Answer: Ustawić kursor na znaku, który chce się zastąpić -> R -> docelowy znak
  ```
- substitute a whole expression
  ```text
  Answer: :%s/co chcemy zastąpić/czym chcemy zastąpić/g
  ```
- save changes
  ```text
  Answer: ESC -> :w -> ENTER
  ```
- exit Vim (2 ways)
  ```text
  Answer: ESC -> :q -> ENTER lub ESC -> :x -> Enter (Zapisz i zamknij)
  ```

