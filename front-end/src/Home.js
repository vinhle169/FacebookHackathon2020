import React from 'react';
import { ChatFeed, Message } from 'react-chat-ui';
import styled from 'styled-components';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';

const Style = styled.div`
  .inputBox {
    display: flex;
    flex-direction: row;
  }
`;

const test_messages = [new Message({id: 1, message: "Hello World!", senderName: "Elon Musk"}),
                        new Message({id: 0, message: "Whats up"})]

class Home extends React.Component {
  constructor(props) {
    super(props);
    this.state = {messages: null};
  }

  render() {
    this.state.messages = test_messages
    return (
      <Style>
        <ChatFeed
          messages={this.state.messages}
            bubbleStyles={
            {
            text: {
                fontSize: 30
            },
            chatbubble: {
                borderRadius: 70,
                padding: 40
            }
            }
            }
            showSenderName
        />
        <div className="inputBox">
          <Form>
            <Form.Control type="text" placeholder="Normal text" />
          </Form>
          <Button onClick={} type="submit" className="my-1">
            Send
          </Button>
        </div>
      </Style>
    )
  }
}

export default Home;