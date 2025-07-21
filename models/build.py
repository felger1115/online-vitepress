import os
import subprocess

from utils.logger import logger
    
class Builder:
    """
    用于在 vitepress 目录下执行 npm run docs:build 的工具类。
    """
    @staticmethod
    def build_docs(path=None):
        path = path or 'view'
        vitepress_dir = os.path.join(os.path.dirname(__file__), '..', path)
        vitepress_dir = os.path.abspath(vitepress_dir)
        try:
            result = subprocess.run(
                ['npm', 'run', 'docs:build'],
                cwd=vitepress_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            if result.returncode == 0:
                logger.info('打包成功')
                logger.info(result.stdout)
                return True
            else:
                logger.error('打包失败:')
                logger.error(result.stderr)
                return False
        except Exception as e:
            logger.error(f'执行打包命令异常: {e}')
            return False
