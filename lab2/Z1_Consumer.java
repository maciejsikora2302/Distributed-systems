import com.rabbitmq.client.AMQP;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.Consumer;
import com.rabbitmq.client.DefaultConsumer;
import com.rabbitmq.client.Envelope;
import java.io.IOException;

public class Z1_Consumer {

    public static void main(String[] argv) throws Exception {

        // info
        System.out.println("Z1 CONSUMER");

        // connection & channel
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("localhost");
        Connection connection = factory.newConnection();
        Channel channel = connection.createChannel();

        // queue
        String QUEUE_NAME = "queue1";
        channel.queueDeclare(QUEUE_NAME, false, false, false, null);
        channel.basicQos(1);


        // consumer (handle msg)
        Consumer consumer = new DefaultConsumer(channel) {
            @Override
            public void handleDelivery(String consumerTag, Envelope envelope, AMQP.BasicProperties properties, byte[] body) throws IOException {
//                channel.basicAck(envelope.getDeliveryTag(), false);
                String message = new String(body, "UTF-8");
                int timeToSleep = Integer.parseInt(message);
                System.out.println("Parsing message("+timeToSleep+")...");
                try {
                    Thread.sleep(timeToSleep * 1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                System.out.println("Done.");
                channel.basicAck(envelope.getDeliveryTag(), false);
            }
        };

        // start listening

        System.out.println("Waiting for messages...");
        channel.basicConsume(QUEUE_NAME, false, consumer);

//        channel.basicConsume(QUEUE_NAME, true, consumer);


        // close
//        channel.close();
//        connection.close();
    }
}
