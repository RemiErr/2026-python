# TEST_CASES

以下為自訂測資（請執行後填入「實際結果」與 PASS/FAIL）：

1. 正常情況
- 輸入：`(1,1,N)`, 指令 `FFRFF`
- 預期結果：位置 `(3,3)`、方向 `E`、未 LOST
- 實際結果：位置 `(3,3)`、方向 `E`、未 LOST
- PASS/FAIL：PASS
- 對應測試函式：`test_forward_within_bounds`

2. 邊界情況
- 輸入：`(0,9,N)`, 指令 `F`
- 預期結果：`LOST`（邏輯座標 0..9）
- 實際結果：`LOST`
- PASS/FAIL：PASS
- 對應測試函式：`test_lost_stops_future_commands`

3. 反例（容易寫錯）
- 輸入：`(0,0,N)`, 指令 `RRRR`
- 預期結果：方向回到 `N`
- 實際結果：方向回到 `N`
- PASS/FAIL：PASS
- 對應測試函式：`test_four_rights_returns`

4. scent 方向差異
- 輸入：`(0,9,N) F` 後，再 `reset (0,9,E)` 再 `F`
- 預期結果：第二台不會因 `N` 的 scent 被阻擋
- 實際結果：第二台不會因 `N` 的 scent 被阻擋
- PASS/FAIL：PASS
- 對應測試函式：`test_same_cell_different_dir_not_blocked`

5. LOST 後仍有後續指令
- 輸入：`(0,9,N)`, 指令 `FRF`
- 預期結果：第一次 `F` LOST，後續指令被忽略
- 實際結果：第一次 `F` LOST，後續指令被忽略
- PASS/FAIL：PASS
- 對應測試函式：`test_lost_stops_future_commands`

6. scent 生效
- 輸入：`(0,9,N) F`（第一台 LOST 留 scent）
  再 `reset (0,9,N)`，指令 `F`
- 預期結果：第二台忽略 `F`，不 LOST
- 實際結果：第二台忽略 `F`，不 LOST
- PASS/FAIL：PASS
- 對應測試函式：`test_scent_blocks_forward`

7. 非法指令
- 輸入：`(1,1,E)`, 指令 `X`
- 預期結果：忽略指令，狀態不變
- 實際結果：忽略指令，狀態不變
- PASS/FAIL：PASS
- 對應測試函式：`test_invalid_command_is_ignored`

8. 邊界內移動不會 LOST
- 輸入：`(1,1,N)`, 指令 `F`
- 預期結果：位置 `(1,2)`、未 LOST
- 實際結果：位置 `(1,2)`、未 LOST
- PASS/FAIL：PASS
- 對應測試函式：`test_forward_within_bounds`
