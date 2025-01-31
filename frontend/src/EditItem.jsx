import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";

export default function EditItem() {
  const { id } = useParams(); // Get item ID from URL
  const navigate = useNavigate();

  const [item, setItem] = useState({
    name: "",
    icon: "",
    notes: "",
    url: "",
    username: "",
    password: "",
  });

  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  // Fetch item data on mount
  useEffect(() => {
    fetch(`http://localhost:8000/api/v1/password/${id}/`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`, // Ensure authentication
      },
    })
      .then((res) => res.json())
      .then((data) => setItem(data))
      .catch(() => setError("Failed to load item"));
  }, [id]);

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch(
        `http://localhost:8000/api/v1/password/${id}/`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`, // Auth token
          },
          body: JSON.stringify(item),
        },
      );

      if (response.ok) {
        setSuccess(true);
        setTimeout(() => navigate("/items"), 2000); // Redirect after 2 seconds
      } else {
        setError("Failed to update item.");
      }
    } catch {
      setError("Something went wrong.");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-6 rounded-lg shadow-lg w-96">
        <h2 className="text-2xl font-bold text-center mb-4">Edit Item</h2>

        {success && (
          <p className="text-green-600 text-center">✅ Updated successfully!</p>
        )}
        {error && <p className="text-red-500 text-center">{error}</p>}

        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="text"
            placeholder="Name"
            className="w-full px-4 py-2 border rounded-md"
            value={item.name}
            onChange={(e) => setItem({ ...item, name: e.target.value })}
            required
          />

          <input
            type="text"
            placeholder="Icon"
            className="w-full px-4 py-2 border rounded-md"
            value={item.icon}
            onChange={(e) => setItem({ ...item, icon: e.target.value })}
          />

          <textarea
            placeholder="Notes"
            className="w-full px-4 py-2 border rounded-md"
            value={item.notes}
            onChange={(e) => setItem({ ...item, notes: e.target.value })}
          />

          <input
            type="url"
            placeholder="URL"
            className="w-full px-4 py-2 border rounded-md"
            value={item.url}
            onChange={(e) => setItem({ ...item, url: e.target.value })}
          />

          <input
            type="text"
            placeholder="Username"
            className="w-full px-4 py-2 border rounded-md"
            value={item.username}
            onChange={(e) => setItem({ ...item, username: e.target.value })}
            required
          />

          <input
            type="password"
            placeholder="Password"
            className="w-full px-4 py-2 border rounded-md"
            value={item.password}
            onChange={(e) => setItem({ ...item, password: e.target.value })}
            required
          />

          <button
            type="submit"
            className="w-full bg-blue-500 text-white px-4 py-2 rounded-md"
          >
            Update Item
          </button>
        </form>

        <button
          onClick={() => navigate("/items")}
          className="mt-4 text-blue-500 text-center w-full"
        >
          Cancel
        </button>
      </div>
    </div>
  );
}
