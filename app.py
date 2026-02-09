from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import redis
import os
import socket
import uvicorn

app = FastAPI(
    title="DevOps Visit Counter API",
    description="Application de compteur de visites avec FastAPI et Redis",
    version="1.0.0"
)

# Connexion Redis
redis_host = os.getenv('REDIS_HOST', 'localhost')
try:
    r = redis.Redis(
        host=redis_host,
        port=6379,
        db=0,
        decode_responses=True,
        socket_connect_timeout=3,
        socket_timeout=3
    )
    r.ping()
    redis_connected = True
    redis_status = "✅ Connecté"
except Exception as e:
    redis_connected = False
    redis_status = f"❌ Erreur: {str(e)}"

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Page d'accueil principale avec compteur"""
    hostname = socket.gethostname()
    
    if redis_connected:
        visits = r.incr('visits_counter')
        counter_text = f"👁️ Visite #{visits}"
    else:
        visits = "N/A"
        counter_text = "🔴 Service indisponible"
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>DevOps Project - FastAPI & Docker</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }}
            
            .container {{
                background: rgba(255, 255, 255, 0.95);
                border-radius: 20px;
                padding: 40px;
                max-width: 900px;
                width: 100%;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                backdrop-filter: blur(10px);
            }}
            
            .header {{
                text-align: center;
                margin-bottom: 40px;
                border-bottom: 3px solid #667eea;
                padding-bottom: 20px;
            }}
            
            h1 {{
                color: #2d3748;
                font-size: 2.8rem;
                margin-bottom: 10px;
                background: linear-gradient(90deg, #667eea, #764ba2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}
            
            .subtitle {{
                color: #718096;
                font-size: 1.2rem;
                font-weight: 500;
            }}
            
            .counter {{
                text-align: center;
                margin: 40px 0;
                padding: 30px;
                background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            }}
            
            .counter-number {{
                font-size: 5rem;
                font-weight: bold;
                color: #2d3748;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
            }}
            
            .counter-label {{
                font-size: 1.5rem;
                color: #4a5568;
                margin-top: 10px;
            }}
            
            .info-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin: 40px 0;
            }}
            
            .info-card {{
                background: #f7fafc;
                padding: 25px;
                border-radius: 12px;
                border-left: 5px solid #667eea;
                transition: transform 0.3s ease;
            }}
            
            .info-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
            }}
            
            .info-title {{
                color: #4a5568;
                font-size: 1.1rem;
                font-weight: 600;
                margin-bottom: 10px;
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            
            .info-value {{
                color: #2d3748;
                font-size: 1.3rem;
                font-weight: bold;
            }}
            
            .tech-stack {{
                margin-top: 40px;
            }}
            
            .tech-title {{
                color: #4a5568;
                font-size: 1.3rem;
                margin-bottom: 20px;
                text-align: center;
            }}
            
            .tech-badges {{
                display: flex;
                flex-wrap: wrap;
                gap: 15px;
                justify-content: center;
            }}
            
            .badge {{
                background: #e2e8f0;
                color: #2d3748;
                padding: 10px 20px;
                border-radius: 25px;
                font-weight: 600;
                font-size: 0.9rem;
                transition: all 0.3s ease;
            }}
            
            .badge:hover {{
                background: #667eea;
                color: white;
                transform: scale(1.05);
            }}
            
            .instructions {{
                background: #e6fffa;
                border-left: 5px solid #38b2ac;
                padding: 20px;
                border-radius: 10px;
                margin-top: 30px;
            }}
            
            .footer {{
                text-align: center;
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #e2e8f0;
                color: #718096;
                font-size: 0.9rem;
            }}
            
            @media (max-width: 768px) {{
                .container {{
                    padding: 20px;
                }}
                
                h1 {{
                    font-size: 2rem;
                }}
                
                .counter-number {{
                    font-size: 3.5rem;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 Projet DevOps</h1>
                <p class="subtitle">Compteur de visites avec FastAPI & Docker</p>
            </div>
            
            <div class="counter">
                <div class="counter-number">{counter_text}</div>
                <div class="counter-label">Nombre total de visites</div>
            </div>
            
            <div class="info-grid">
                <div class="info-card">
                    <div class="info-title">🏗️ Infrastructure</div>
                    <div class="info-value">Docker & Docker Compose</div>
                </div>
                
                <div class="info-card">
                    <div class="info-title">⚡ Backend</div>
                    <div class="info-value">FastAPI (Python)</div>
                </div>
                
                <div class="info-card">
                    <div class="info-title">💾 Base de données</div>
                    <div class="info-value">Redis</div>
                    <div style="margin-top: 10px; font-size: 0.9rem; color: {'#38a169' if redis_connected else '#e53e3e'};">
                        {redis_status}
                    </div>
                </div>
                
                <div class="info-card">
                    <div class="info-title">🖥️ Serveur</div>
                    <div class="info-value">{hostname}</div>
                </div>
            </div>
            
            <div class="tech-stack">
                <div class="tech-title">🛠️ Stack Technologique</div>
                <div class="tech-badges">
                    <span class="badge">FastAPI</span>
                    <span class="badge">Docker</span>
                    <span class="badge">Docker Compose</span>
                    <span class="badge">Redis</span>
                    <span class="badge">Python 3.9</span>
                    <span class="badge">Uvicorn</span>
                    <span class="badge">HTML5/CSS3</span>
                    <span class="badge">Linux</span>
                </div>
            </div>
            
            <div class="instructions">
                <p><strong>💡 Instructions :</strong></p>
                <p>• Rafraîchissez la page (F5) pour augmenter le compteur</p>
                <p>• Testez l'API : <a href="/docs">/docs</a> (Swagger UI)</p>
                <p>• Vérifiez la santé : <a href="/health">/health</a></p>
                <p>• Voir les métriques : <a href="/metrics">/metrics</a></p>
            </div>
            
            <div class="footer">
                <p>📅 Projet créé le : {os.environ.get('BUILD_DATE', '2025')}</p>
                <p>👨‍💻 Développeur DevOps : [Safa Labidi]</p>
                <p>⚡ Chaque visite est persistée dans Redis</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

@app.get("/health")
async def health_check():
    """Endpoint de vérification de santé"""
    health_status = {
        "status": "healthy" if redis_connected else "unhealthy",
        "service": "devops-visit-counter",
        "redis": "connected" if redis_connected else "disconnected",
        "timestamp": __import__('datetime').datetime.now().isoformat()
    }
    
    if redis_connected:
        return health_status
    else:
        return health_status, 503

@app.get("/metrics")
async def get_metrics():
    """Endpoint de métriques"""
    if redis_connected:
        visits = r.get('visits_counter') or 0
        try:
            visits = int(visits)
        except:
            visits = 0
    else:
        visits = "N/A"
    
    return {
        "service": "devops-visit-counter",
        "total_visits": visits,
        "redis_connected": redis_connected,
        "server_hostname": socket.gethostname(),
        "uptime": __import__('time').time() - __import__('psutil').boot_time() if __import__('sys').modules.get('psutil') else "N/A"
    }

@app.get("/debug/redis")
async def debug_redis():
    """Route de débogage pour voir le contenu de Redis"""
    if not redis_connected:
        return {"error": "Redis non connecté"}
    
    # Récupère toutes les clés
    keys = r.keys('*')
    
    # Récupère les valeurs
    data = {}
    for key in keys:
        data[key] = r.get(key)
    
    return {
        "total_keys": len(keys),
        "keys": keys,
        "data": data,
        "visits_counter": r.get('visits_counter')
    }

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=5000,
        reload=True,
        log_level="info"
    )