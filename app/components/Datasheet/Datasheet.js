import React from 'react';
import axios from 'axios';

class Datasheet extends React.Component {
  state = {
    message: 'None received'
  }

  componentDidMount() {
    this.request();
  }

  request = () => {
    const { getAccessToken } = this.props.auth;
    const API_URL = 'http://localhost:3000/api';
    const headers = { 'Authorization': `Bearer ${getAccessToken()}`}
    axios.get(`${API_URL}/private`, { headers })
      .then((response) => 
        {
          this.setState({ message: response.data })
        })
      .catch((error) => {
        this.setState({ message: error.message })
    });
  }

  render() {
    return (
      <div>
        Here be Datasheet.
        <br />
        Message: {this.state.message}
      </div>
    );
  }
}

export default Datasheet;
