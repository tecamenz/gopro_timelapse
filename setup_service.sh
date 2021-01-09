cp gopro_timelapse_service.service /lib/systemd/system/gopro_timelapse_service.service
chmod 755 /lib/systemd/system/gopro_timelapse_service.service
systemctl daemon-reload
systemctl enable gopro_timelapse_service.service
systemctl start gopro_timelapse_service.service

