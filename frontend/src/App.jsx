import { useState } from 'react'
import ItemList from './ItemList'

function App() {

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/items" element={<ItemList />} />
      </Routes>
    </Router>
  )
}

export default App
