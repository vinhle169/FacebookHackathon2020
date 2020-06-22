import React from 'react';
import { ChatFeed, Message } from 'react-chat-ui';
import styled from 'styled-components';
import InputGroup from 'react-bootstrap/InputGroup'
import Form from 'react-bootstrap/Form';
import FormControl from 'react-bootstrap/FormControl';
import Button from 'react-bootstrap/Button';
import io from 'socket.io-client';

const Style = styled.div`
  .inputBox {
    display: flex;
    flex-direction: row;
  }

  .sendButton {

  }
`;

const test_messages = [new Message({id: 1, message: "Hello World!", senderName: "Heal-Bot"}),
                        new Message({id: 0, message: "Whats up"})]

class Home extends React.Component {
  constructor(props) {
    super(props);
    this.state = {messages: test_messages, nextMessage: ""};
    this.sendHandler = this.sendHandler.bind(this);
    this.changeHandler = this.changeHandler.bind(this);
  }

  componentDidMount() {
    this.endpoint = 'localhost:8008';
    this.socket = io(this.endpoint);
    this.user_id = 'FIXME'  // FIX ME
    this.socket.emit('join', {user_id: this.user_id});
    this.socket.on('loadPast', (messages) => {
      this.setState({ messages });
    });
    this.socket.on('response', (message) => {
      this.receiveMessage(message);
    });
    console.log(this.socket);
  }

  componentWillUnmount() {
    this.socket.emit('disconnect');
    this.socket.off()
  }

  changeHandler(event) {
    console.log(event.target.value)
    this.setState({nextMessage: event.target.value});
  }

  receiveMessage(message) {
    let newMessage = new Message({id: 1, message })
    this.setState({messages: this.state.messages.concat(newMessage)})
  }

  sendHandler(event) {
    event.preventDefault();
    let newMessage = new Message({id: 0, message: this.state.nextMessage});
    this.setState({messages: this.state.messages.concat(newMessage)});
    this.socket.emit('message', {message: this.state.nextMessage})
  }

  render() {
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
        <Form onSubmit={this.sendHandler}>
          <InputGroup>
            <FormControl
              placeholder="Send a message..."
              onChange={this.changeHandler}
            />
            <InputGroup.Append>
              <Button variant="outline-secondary" type="submit" className="sendButton">Send</Button>
            </InputGroup.Append>
          </InputGroup>
        </Form>
      </Style>
    )
  }
}

export default Home;