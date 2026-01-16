import subprocess
from datetime import datetime, timedelta
import sys

def analyze_git_time():
    try:
        # Obtener el log de git: Autor | Fecha
        cmd = ['git', 'log','--all', '--pretty=format:%an|%ad', '--date=iso']
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode != 0:
            print("Error ejecutando git log. Asegúrate de que es un repositorio git válido.")
            return

        lines = result.stdout.strip().split('\n')
        commits_by_author = {}

        for line in lines:
            if not line: continue
            try:
                parts = line.split('|')
                if len(parts) < 2: continue
                author = parts[0].strip()
                date_str = parts[1].strip()
                # Parsear fecha ISO (e.g., 2023-01-01 12:00:00 +0100)
                # Simplificación: tomamos hasta los segundos y permitimos que python maneje el offset si es reciente,
                # o ignoramos el offset para el cálculo relativo simple.
                dt = datetime.fromisoformat(date_str)
                
                if author not in commits_by_author:
                    commits_by_author[author] = []
                commits_by_author[author].append(dt)
            except Exception as e:
                continue

        print(f"{'AUTOR':<25} | {'TIEMPO ESTIMADO':<20} | {'COMMITS':<10}")
        print("-" * 60)

        # Configuración de la heurística
        SESSION_THRESHOLD = timedelta(hours=3) # Si pasa mas de esto, es nueva sesión
        BASE_COMMIT_TIME = timedelta(minutes=30) # Tiempo base por commit aislado o inicio de sesión

        for author, dates in commits_by_author.items():
            if not dates: continue
            dates.sort()
            
            total_time = timedelta()
            
            # El primer commit siempre inicia una sesión
            current_session_start = dates[0]
            last_commit_time = dates[0]
            total_time += BASE_COMMIT_TIME 
            
            for i in range(1, len(dates)):
                current = dates[i]
                diff = current - last_commit_time
                
                if diff < SESSION_THRESHOLD:
                    # Dentro de la misma sesión, sumamos la diferencia real
                    total_time += diff
                else:
                    # Nueva sesión, sumamos tiempo base
                    total_time += BASE_COMMIT_TIME
                
                last_commit_time = current

            # Formatear tiempo total
            total_seconds = int(total_time.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            
            time_str = f"{hours}h {minutes}m"
            print(f"{author:<25} | {time_str:<20} | {len(dates):<10}")

    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    analyze_git_time()
