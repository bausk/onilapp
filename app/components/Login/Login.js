import React from 'react';

class Login extends React.Component {

  state = {
    result: null
  };

  login = (e) => {
    this.props.auth.login();
    // const endpoint = 'http://localhost:3000/api/public';
    // const { data } = await axios.get(
    //   endpoint
    // );
    // this.setState({
    //   result: JSON.stringify(data)
    // });
  }

  logout = (e) => {
    this.props.auth.logout();
    // const endpoint = 'http://localhost:3000/api/public';
    // const { data } = await axios.get(
    //   endpoint
    // );
    // this.setState({
    //   result: JSON.stringify(data)
    // });
  }

  render() {
    const isAuthenticated = this.props.auth && this.props.auth.isAuthenticated;
    return (
      <div>
        <div>Ternovka-2 Landing Page</div>
        <div>{isAuthenticated() ? 
          <button onClick={this.logout}>
            Log Out
          </button> : 
          <button onClick={this.login}>
            Log In
          </button>
        }
        </div>
      </div>
    );
  }
}

export default Login;
