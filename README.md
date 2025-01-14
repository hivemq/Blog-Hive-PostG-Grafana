#Introduction


Operational data is the new gold but is only valuable if it’s easily accessible and interpretable. MQTT is the method to harvest your valuable data and Grafana is the tool to visualise the information to really make it work for you. In this blog we show how easy this pipeline can be set up and put to actual use.

 
#Goals

MQTT data visualization is essential for transforming raw MQTT message streams into meaningful insights, enabling users to monitor, analyze, and act on real-time data effectively.

The combination of MQTT (Message Queuing Telemetry Transport) along with HiveMQ brokers Postgress databases and Grafana offers a robust, efficient, and flexible solution for gathering, visualizing and analyzing data. 

MQTT, a lightweight and efficient messaging protocol, is specifically designed for constrained networks and devices, making it ideal for IoT applications. 

Grafana is a powerful visualization and analytics platform that excels at turning raw data into meaningful insights through customizable and interactive dashboards.

In order to do long-term storage and offer direct integration with visualisation systems such as Grafana a intermediate Postgress database is used. Both HiveMQ brokers and Grafa integrate very good with this open source platform.

By integrating MQTT and Grafana, you can create a seamless pipeline for collecting real-time data from sensors, devices, or applications, and then visualizing it in an intuitive and user-friendly interface. This combination is particularly effective in scenarios such as smart home systems, industrial automation, environmental monitoring, and any application where timely and actionable insights are critical.

Rollout: 

docker-compose up --build -d      
sleep 30
curl  -X POST localhost:8888/api/v1/data-hub/management/start-trial

mqtt hivemq schema create --id=mytemp-in-schema  --file=mytemp-in-schema.json --type=json
mqtt hivemq schema create --id=mytemp-out-schema --file=mytemp-out-schema.json --type=json
mqtt hivemq script create --id=add_timestamp --file=add_timestamp.js --type=transformation
mqtt hivemq data-policy create --file=add_ts_policy.json  

mqtt pub -t temp/test --message-file=mytemp.json 
