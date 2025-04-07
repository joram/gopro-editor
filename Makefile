deploy:
	cd frontend && npm run build
	cd backend && cp -r ../frontend/dist/* ./static/
	cd backend && docker build -t joram87/gopro-editor:latest .
	docker push joram87/gopro-editor:latest
	ssh saintNectaire "cd projects/nas; docker compose pull gopro-editor; docker compose up -d gopro-editor --remove-orphans; docker compose logs -f gopro-editor"