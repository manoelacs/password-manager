import ItemList from './ItemList';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './Login';

function App() {
  return (
    <Router>
      <Routes>
        <Route path='/' element={<Login />} />
        <Route path='/login' element={<Login />} />
        <Route path='/items' element={<ItemList />} />
      </Routes>
    </Router>
  );
}

export default App;
