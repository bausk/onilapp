import React, { Component } from 'react';
import styled from 'styled-components';
import Header from '../components/Header/Header.js';
import Datasheet from '../components/Datasheet/Datasheet';
import Plot from '../components/Plot/Plot';

const AppWrapper = styled.div`
  text-align: center;
  padding: 20px;
`;

const Body = styled.div`
  padding-top: 20px;
  padding-bottom: 20px;
  text-align: center;
  font-size: 22px;
  border-color: rgb(211, 211, 211);
  border-style: solid;
  border-width: 1px;
  border-top-width: 0;
`;

class App extends Component {
  state = {
    tabs: [
      {
        id: 0,
        title: 'Datasheet'
      },
      {
        id: 1,
        title: 'Plot'
      }],
    selectedTab: null
  };

  onSelect = (selected) => {
    if (this.state.tabs.some(t => t.id === selected)) {
      this.setState({ selectedTab: selected });
    }
  };

  render() {
    return (
      <AppWrapper>
        <Header
          tabs={this.state.tabs}
          selected={this.state.selectedTab}
          onSelect={this.onSelect}
        />
        <Body>
          {(this.state.selectedTab === 0) && <Datasheet />}
          {(this.state.selectedTab === 1) && <Plot />}
        </Body>
      </AppWrapper>
    );
  }
}

export default App;
