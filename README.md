# Coverage-based Testcase Selector

カバレッジに寄与しないテストケースを削除するツール

## Introduction
python 3.8.10, python 3.9.6で動作確認済み。  
シェルは全てpowershellを使用しています。
- pythonモジュールのインストール
    ```
    > pip install -r requirements.txt
    ```
- 外部モジュールのダウンロード
    ```
    > setup.ps1
    ```
- fizzbuzzプロジェクトを用いたデモの実行
    ```
    > demo.ps1
    ```

## How to Use
```
> python path/to/coverage-based-selector/src/main.py -t TARGET_SOURCE_PATH --classpath CLASSPATH --sourcepath SOURCEPATH [--additional_test_path ADDITIONAL_TEST_PATH] [--remain_temp] [--temp TEMPFOLDER] -o OUTPUT_DIR junit_testsuite_path
```