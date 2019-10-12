source activate /annoroad/data1/bioinfo/PMO/yangmengcheng/SoftWare/Anaconda3-5.3.1/envs/RockMind_V3
nginx=/annoroad/data1/bioinfo/PMO/yangmengcheng/SoftWare/Nginx-1.16/sbin/nginx
uwsgi_conf=/annoroad/data1/bioinfo/PMO/yangmengcheng/Work/RockMind/visualization_v3/uwsgi
for i in "$*";
do
	case $i in
		reload)
			$nginx -s reload 
			uwsgi --reload $uwsgi_conf/uwsgi.pid	
			echo "reload server done!"
		;;
		start)
			$nginx
			uwsgi --ini $uwsgi_conf/uwsgi.ini
			echo "start server done!"
		;;
		stop)
			$nginx -s stop
			uwsgi --stop $uwsgi_conf/uwsgi.pid
			echo "stop uwsgi server done!"
		;;
		?)
			echo "参数有误"
		exit 1 ;;
	esac
done
