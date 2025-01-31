import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom"; // Redirect users

export default function ItemList() {
  const [items, setItems] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    checkAuth(); // Check authentication before fetching data
    fetchItems();
  }, [searchQuery, currentPage]);

  // Check if user is authenticated
  const checkAuth = () => {
    const token = localStorage.getItem("token"); // Get token from localStorage
    if (!token) {
      navigate("/login"); // Redirect to login if no token
    }
  };

  // Fetch items from Django API
  const fetchItems = async () => {
    const token = localStorage.getItem("token");

    try {
      const response = await fetch(
        `http://localhost:8000/api/v1/passwords/?search=${searchQuery}&page=${currentPage}`,
        {
          headers: {
            Authorization: `Bearer ${token}`, // Include token in request headers
          },
        },
      );

      if (response.status === 401) {
        navigate("/login"); // Redirect to login if unauthorized
      }

      const data = await response.json();
      setItems(data.results);
      setTotalPages(Math.ceil(data.count / 5)); // Adjust based on page size
    } catch (err) {
      setError("Failed to fetch items.");
    }
  };

  // Handle Delete Item
  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this item?")) return;

    const token = localStorage.getItem("token");

    try {
      const response = await fetch(
        `http://localhost:8000/api/v1/password/${id}/`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`, // Include token in request
          },
        },
      );

      if (response.ok) {
        fetchItems();
      } else {
        setError("Failed to delete item.");
      }
    } catch (err) {
      setError("Error deleting item.");
    }
  };

  // Handle Edit Item (Redirect to Edit Page)
  const handleEdit = (id) => {
    navigate(`/edit/${id}`);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-6">
      <h1 className="text-2xl font-bold mb-4">Item List</h1>

      {/* Search Bar */}
      <input
        type="text"
        className="w-full max-w-md px-4 py-2 mb-4 border rounded-lg"
        placeholder="Search items..."
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
      />

      {error && <p className="text-red-500">{error}</p>}

      <div className="w-full max-w-3xl bg-white p-4 rounded-lg shadow-lg">
        {items.length === 0 ? (
          <p className="text-gray-600">No items found.</p>
        ) : (
          <ul className="space-y-4">
            {items.map((item) => (
              <li
                key={item.id}
                className="flex justify-between items-center bg-gray-50 p-3 rounded-lg shadow"
              >
                <div>
                  <p className="font-medium">{item.name}</p>
                  <p className="text-gray-500 text-sm">{item.notes}</p>
                </div>
                <div className="flex space-x-2">
                  <button
                    onClick={() => handleEdit(item.id)}
                    className="bg-blue-500 text-white px-3 py-1 rounded-md"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDelete(item.id)}
                    className="bg-red-500 text-white px-3 py-1 rounded-md"
                  >
                    Delete
                  </button>
                </div>
              </li>
            ))}
          </ul>
        )}

        {/* Pagination Controls */}
        <div className="flex justify-center mt-4 space-x-2">
          <button
            className={`px-3 py-1 rounded-md ${currentPage === 1 ? "bg-gray-300" : "bg-gray-700 text-white"}`}
            onClick={() => setCurrentPage(currentPage - 1)}
            disabled={currentPage === 1}
          >
            Previous
          </button>
          <span className="px-3 py-1 bg-gray-200 rounded-md">
            Page {currentPage} of {totalPages}
          </span>
          <button
            className={`px-3 py-1 rounded-md ${currentPage === totalPages ? "bg-gray-300" : "bg-gray-700 text-white"}`}
            onClick={() => setCurrentPage(currentPage + 1)}
            disabled={currentPage === totalPages}
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
}
