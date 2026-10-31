pipeline {
    agent any

    environment {
        PYTHONUNBUFFERED = '1'
        BACKEND_IMAGE = 'belajar-backend'
        BACKEND_CONTAINER = 'guestbook-backend'
        FRONTEND_CONTAINER = 'guestbook-frontend'
        VOLUME_NAME = 'guestbook-db-data'
        NETWORK_NAME = 'app-net'
    }

    stages {
        stage('1. Checkout') {
            steps {
                echo '=== [STAGE 1: CHECKOUT] Mengunduh source code dari branch main ==='
                checkout scm
                sh 'git log -1 --oneline'
            }
        }

        stage('2. Syntax Check') {
            steps {
                echo '=== [STAGE 2: SYNTAX CHECK] Validasi sintaks Python & Docker Compose ==='
                sh '''
                echo "1. Memeriksa sintaks Python app.py..."
                python3 -m py_compile app.py
                
                echo "2. Menjalankan automated unit test test_app.py..."
                python3 -m unittest test_app.py -v
                
                echo "3. Memvalidasi sintaks berkas docker-compose.yml..."
                if command -v docker-compose >/dev/null 2>&1; then
                    docker-compose config -q
                elif docker compose version >/dev/null 2>&1; then
                    docker compose config -q
                fi
                echo "Seluruh pemeriksaan sintaks berhasil!"
                '''
            }
        }

        stage('3. Build Image') {
            steps {
                echo '=== [STAGE 3: BUILD IMAGE] Membangun image Docker backend ==='
                sh '''
                SHORT_SHA=$(git rev-parse --short HEAD 2>/dev/null || echo "latest")
                echo "Building backend Docker image (tag: ${BUILD_NUMBER} dan ${SHORT_SHA})..."
                docker build -t ${BACKEND_IMAGE}:${BUILD_NUMBER} -t ${BACKEND_IMAGE}:latest -t ${BACKEND_IMAGE}:${SHORT_SHA} .
                '''
            }
        }

        stage('4. Automated Deployment') {
            steps {
                echo '=== [STAGE 4: AUTOMATED DEPLOYMENT] Menjalankan pembaruan stack kontainer ==='
                sh '''
                echo "Memastikan Docker Bridge Network ${NETWORK_NAME} tersedia..."
                docker network create ${NETWORK_NAME} 2>/dev/null || true
                docker network connect ${NETWORK_NAME} jenkins-server 2>/dev/null || true

                echo "Memastikan Docker Named Volume ${VOLUME_NAME} dipertahankan..."
                docker volume create ${VOLUME_NAME}

                echo "Memperbarui kontainer backend tanpa menghapus data..."
                docker stop ${BACKEND_CONTAINER} 2>/dev/null || true
                docker rm ${BACKEND_CONTAINER} 2>/dev/null || true
                
                docker run -d \
                    --name ${BACKEND_CONTAINER} \
                    --network ${NETWORK_NAME} \
                    --network-alias backend \
                    -p 8000:8000 \
                    -v ${VOLUME_NAME}:/var/lib/backend_data \
                    --restart unless-stopped \
                    ${BACKEND_IMAGE}:latest

                echo "Memastikan kontainer frontend Nginx tetap aktif melayani UI..."
                docker restart ${FRONTEND_CONTAINER} 2>/dev/null || true
                '''
            }
        }

        stage('5. Health Check') {
            steps {
                echo '=== [STAGE 5: HEALTH CHECK] Verifikasi kesiapan layanan (API & UI) ==='
                sh '''
                echo "Menunggu kesiapan backend service (3 detik)..."
                sleep 3

                echo "Uji 1: Memeriksa endpoint /health..."
                for i in 1 2 3 4 5; do
                    if curl -fsS http://${BACKEND_CONTAINER}:8000/health >/dev/null 2>&1 || curl -fsS http://localhost:8000/health >/dev/null 2>&1; then
                        echo "Backend /health OK!"
                        break
                    fi
                    echo "Mencoba kembali ($i/5)..."
                    sleep 2
                done

                echo "Uji 2: Memeriksa endpoint /messages (GET)..."
                curl -fsS http://${BACKEND_CONTAINER}:8000/messages || curl -fsS http://localhost:8000/messages

                echo "Uji 3: Memeriksa Frontend Nginx..."
                curl -fsSI http://${FRONTEND_CONTAINER}:80/ || curl -fsSI http://localhost:8081/

                echo "Menampilkan 10 baris terakhir log backend..."
                docker logs --tail 10 ${BACKEND_CONTAINER}
                '''
            }
        }
    }

    post {
        success {
            echo '========================================================================'
            echo ' CI/CD PIPELINE SUKSES: Aplikasi Buku Tamu Digital Berhasil Di-deploy!'
            echo ' Frontend UI : http://localhost:8081'
            echo ' Backend API : http://localhost:8000/messages'
            echo ' Health Check: http://localhost:8000/health'
            echo ' Data Volume : guestbook-db-data (TERJAGA & AMAN)'
            echo '========================================================================'
        }
        failure {
            echo '========================================================================'
            echo ' CI/CD PIPELINE GAGAL: Periksa Console Output untuk rincian error.'
            echo '========================================================================'
        }
    }
}
