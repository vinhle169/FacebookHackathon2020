import React from 'react';
import { PageNotFound } from './PageNotFound';
import Home from './Home';
import './App.css';
import {BrowserRouter as Router, Route, Switch} from 'react-router-dom';

function App() {
  return (
    <React.Fragment>
      <Router>
        <Switch>
          <Route exact path="/" component={Home} />
          <Route component={PageNotFound} />
        </Switch>
      </Router>
    </React.Fragment>
  );
}

export default App;
