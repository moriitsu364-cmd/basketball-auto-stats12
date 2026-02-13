#!/usr/bin/env python3
"""
バスケットボール統計システム - セットアップスクリプト
"""
import os
import sys
import subprocess
from pathlib import Path
import shutil


def print_header(text):
    """ヘッダーを表示"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def check_python_version():
    """Pythonバージョンのチェック"""
    print_header("Pythonバージョンのチェック")
    
    version = sys.version_info
    print(f"現在のPythonバージョン: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8以上が必要です")
        return False
    
    print("✅ Pythonバージョン: OK")
    return True


def install_requirements():
    """必要なパッケージをインストール"""
    print_header("パッケージのインストール")
    
    requirements_file = Path("requirements.txt")
    
    if not requirements_file.exists():
        print("❌ requirements.txtが見つかりません")
        return False
    
    try:
        print("パッケージをインストール中...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ パッケージのインストール: 完了")
            return True
        else:
            print(f"❌ インストールエラー: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ インストールエラー: {e}")
        return False


def create_directories():
    """必要なディレクトリを作成"""
    print_header("ディレクトリの作成")
    
    directories = [
        "data",
        "data/images",
        "data/images/players",
        "data/images/staff",
        ".streamlit"
    ]
    
    for directory in directories:
        dir_path = Path(directory)
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ ディレクトリ作成: {directory}")
    
    return True


def setup_config_files():
    """設定ファイルのセットアップ"""
    print_header("設定ファイルのセットアップ")
    
    # secrets.tomlの作成
    secrets_file = Path(".streamlit/secrets.toml")
    secrets_example = Path(".streamlit/secrets.toml.example")
    
    if not secrets_file.exists():
        if secrets_example.exists():
            shutil.copy(secrets_example, secrets_file)
            print("✅ secrets.tomlを作成しました")
            print("⚠️  .streamlit/secrets.tomlを編集してAPIキーとパスワードを設定してください")
        else:
            # デフォルトのsecrets.tomlを作成
            default_secrets = """# Gemini API Key
GEMINI_API_KEY = "your-api-key-here"

# Admin Password Hash (default: tsukuba1872)
ADMIN_PASSWORD_HASH = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"
"""
            with open(secrets_file, 'w', encoding='utf-8') as f:
                f.write(default_secrets)
            print("✅ デフォルトのsecrets.tomlを作成しました")
            print("⚠️  .streamlit/secrets.tomlを編集してAPIキーを設定してください")
    else:
        print("ℹ️  secrets.tomlは既に存在します")
    
    # config.tomlの確認
    config_file = Path(".streamlit/config.toml")
    if not config_file.exists():
        print("⚠️  .streamlit/config.tomlが見つかりません（オプショナル）")
    else:
        print("✅ config.tomlを確認しました")
    
    return True


def apply_fixes():
    """修正版ファイルの適用"""
    print_header("修正版ファイルの適用")
    
    response = input("修正版ファイルを適用しますか？ (y/n): ").lower()
    
    if response != 'y':
        print("ℹ️  修正版ファイルの適用をスキップしました")
        return True
    
    src_dir = Path("src")
    
    # バックアップディレクトリの作成
    backup_dir = Path("src/backup")
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    files_to_fix = [
        ("database.py", "database_fixed.py"),
        ("config.py", "config_fixed.py"),
        ("app.py", "app_fixed.py")
    ]
    
    for original, fixed in files_to_fix:
        original_path = src_dir / original
        fixed_path = src_dir / fixed
        backup_path = backup_dir / original
        
        if not fixed_path.exists():
            print(f"⚠️  {fixed}が見つかりません。スキップします。")
            continue
        
        # バックアップ
        if original_path.exists():
            shutil.copy(original_path, backup_path)
            print(f"📦 {original}をバックアップしました → {backup_path}")
        
        # 修正版を適用
        shutil.copy(fixed_path, original_path)
        print(f"✅ {fixed}を{original}に適用しました")
    
    print("\n✅ すべての修正版ファイルを適用しました")
    print(f"📦 元のファイルは {backup_dir} にバックアップされています")
    
    return True


def verify_installation():
    """インストールの検証"""
    print_header("インストールの検証")
    
    # 必要なモジュールのインポートテスト
    required_modules = {
        'streamlit': 'Streamlit',
        'pandas': 'Pandas',
        'plotly': 'Plotly',
        'PIL': 'Pillow'
    }
    
    all_ok = True
    
    for module, name in required_modules.items():
        try:
            __import__(module)
            print(f"✅ {name}: インストール済み")
        except ImportError:
            print(f"❌ {name}: 未インストール")
            all_ok = False
    
    if all_ok:
        print("\n✅ すべての必要なモジュールがインストールされています")
    else:
        print("\n❌ 一部のモジュールがインストールされていません")
    
    return all_ok


def print_next_steps():
    """次のステップを表示"""
    print_header("次のステップ")
    
    print("""
1. Gemini APIキーの設定:
   - .streamlit/secrets.tomlを開く
   - GEMINI_API_KEYにあなたのAPIキーを設定

2. 管理者パスワードの設定（オプション）:
   - デフォルトパスワード: tsukuba1872
   - 変更する場合は、以下のコマンドでハッシュを生成:
     python -c "import hashlib; print(hashlib.sha256('your-password'.encode()).hexdigest())"
   - .streamlit/secrets.tomlのADMIN_PASSWORD_HASHに設定

3. アプリケーションの起動:
   streamlit run src/app.py

4. ブラウザでアクセス:
   http://localhost:8501

詳細な使い方は README.md と FIX_DOCUMENTATION.md をご覧ください。
""")


def main():
    """メイン処理"""
    print("\n" + "🏀" * 30)
    print("\n  バスケットボール統計システム - セットアップ")
    print("\n" + "🏀" * 30)
    
    # 1. Pythonバージョンのチェック
    if not check_python_version():
        return False
    
    # 2. パッケージのインストール
    if not install_requirements():
        print("\n⚠️  パッケージのインストールに失敗しました")
        print("手動でインストールしてください: pip install -r requirements.txt")
    
    # 3. ディレクトリの作成
    create_directories()
    
    # 4. 設定ファイルのセットアップ
    setup_config_files()
    
    # 5. 修正版ファイルの適用
    apply_fixes()
    
    # 6. インストールの検証
    verify_installation()
    
    # 7. 次のステップを表示
    print_next_steps()
    
    print("\n" + "🏀" * 30)
    print("\n  セットアップが完了しました！")
    print("\n" + "🏀" * 30 + "\n")
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nセットアップを中断しました")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        sys.exit(1)
