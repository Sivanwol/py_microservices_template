from server.app import ApplicationMgr
import json

if ApplicationMgr.application.config['RABBITMQ_ENABLED']== True:
    queue = ApplicationMgr.queue
    mq = ApplicationMgr.mqConnector
    
    @queue(queue_name="on_update_config")
    def on_update_config_callback(ch, method, props, body):
        print(props.correlation_id)
        print(props.reply_to)
    
        data = json.loads(body)
        ch.basic_ack(delivery_tag = method.delivery_tag)
        print(data)
        print("on_update_config_callback")
        mq.send_json(data, exchange='', key=props.reply_to, corr_id=props.correlation_id)
