# type: ignore
import os
import cv2
from django.conf import settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from PIL import Image
import tempfile


def generate_video_thumbnail(video_path: str, output_path: str, time_position: float = 1.0) -> bool:
    """
    動画からサムネイル画像を生成
    
    Args:
        video_path: 動画ファイルのパス
        output_path: 出力画像のパス
        time_position: サムネイルを取得する時間位置（秒）
        
    Returns:
        成功したかどうか
    """
    try:
        # OpenCVで動画を開く
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            return False
        
        # 指定した時間位置に移動
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_number = int(fps * time_position)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        
        # フレームを読み込み
        ret, frame = cap.read()
        if not ret:
            return False
        
        # BGRからRGBに変換
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # PIL Imageに変換
        pil_image = Image.fromarray(frame_rgb)
        
        # サムネイルサイズにリサイズ（アスペクト比を保持）
        pil_image.thumbnail((320, 240), Image.Resampling.LANCZOS)
        
        # 保存
        pil_image.save(output_path, 'JPEG', quality=85)
        
        cap.release()
        return True
        
    except Exception as e:
        print(f"サムネイル生成エラー: {e}")
        return False


def validate_video_file(video_file) -> tuple[bool, str]:
    """
    動画ファイルを検証
    
    Args:
        video_file: アップロードされた動画ファイル
        
    Returns:
        (有効かどうか, エラーメッセージ)
    """
    # ファイルサイズチェック（100MB制限）
    max_size = 100 * 1024 * 1024  # 100MB
    if video_file.size > max_size:
        return False, "動画ファイルサイズは100MB以下にしてください"
    
    # ファイル拡張子チェック
    allowed_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm']
    file_extension = os.path.splitext(video_file.name)[1].lower()
    
    if file_extension not in allowed_extensions:
        return False, f"対応していない動画形式です。対応形式: {', '.join(allowed_extensions)}"
    
    return True, ""


def get_video_duration(video_path: str) -> float:
    """
    動画の長さを取得
    
    Args:
        video_path: 動画ファイルのパス
        
    Returns:
        動画の長さ（秒）
    """
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return 0.0
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        duration = frame_count / fps
        
        cap.release()
        return duration
        
    except Exception:
        return 0.0


def process_video_upload(video_file, post_instance) -> bool:
    """
    動画アップロードを処理
    
    Args:
        video_file: アップロードされた動画ファイル
        post_instance: 投稿インスタンス
        
    Returns:
        成功したかどうか
    """
    try:
        # 動画ファイルを保存
        post_instance.video = video_file
        post_instance.save()
        
        # サムネイルを生成
        video_path = post_instance.video.path
        thumbnail_filename = f"thumbnail_{post_instance.id}.jpg"
        thumbnail_path = os.path.join(settings.MEDIA_ROOT, 'video_thumbnails', thumbnail_filename)
        
        # ディレクトリが存在しない場合は作成
        os.makedirs(os.path.dirname(thumbnail_path), exist_ok=True)
        
        if generate_video_thumbnail(video_path, thumbnail_path):
            # サムネイルを保存
            with open(thumbnail_path, 'rb') as f:
                post_instance.video_thumbnail.save(thumbnail_filename, File(f), save=True)
            
            # 一時ファイルを削除
            os.remove(thumbnail_path)
            return True
        else:
            return False
            
    except Exception as e:
        print(f"動画処理エラー: {e}")
        return False


def get_video_info(video_path: str) -> dict:
    """
    動画の情報を取得
    
    Args:
        video_path: 動画ファイルのパス
        
    Returns:
        動画情報の辞書
    """
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return {}
        
        info = {
            'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'fps': cap.get(cv2.CAP_PROP_FPS),
            'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            'duration': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / cap.get(cv2.CAP_PROP_FPS)
        }
        
        cap.release()
        return info
        
    except Exception:
        return {} 