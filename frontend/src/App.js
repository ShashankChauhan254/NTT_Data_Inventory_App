import React, { useEffect, useState } from "react";
import API from "./api";
import "./App.css";

function App() {
  const [inventory, setInventory] = useState([]);
  const [summary, setSummary] = useState(null);
  const [editId, setEditId] = useState(null);

  const initialFormState = {
    name: "",
    category: "RAW",
    quantity: "",
    threshold: "",
    unit: ""
  };

  const [formData, setFormData] = useState(initialFormState);

  useEffect(() => {
    loadData();
  },);

  const loadData = async () => {
    await Promise.all([fetchInventory(), fetchSummary()]);
  };

  const fetchInventory = async () => {
    try {
      const { data } = await API.get("/inventory");
      setInventory(data);
    } catch (error) {
      console.error("Error fetching inventory:", error);
    }
  };

  const fetchSummary = async () => {
    try {
      const { data } = await API.get("/inventory/summary");
      setSummary(data);
    } catch (error) {
      console.error("Error fetching summary:", error);
    }
  };

  const handleChange = ({ target }) => {
    const { name, value } = target;
    setFormData((prev) => ({
      ...prev,
      [name]: value
    }));
  };

  const resetForm = () => {
    setFormData(initialFormState);
    setEditId(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const payload = {
      ...formData,
      quantity: Number(formData.quantity),
      threshold: Number(formData.threshold)
    };

    try {
      if (editId) {
        await API.put(`/inventory/${editId}`, payload);
      } else {
        await API.post("/inventory", payload);
      }

      resetForm();
      loadData();
    } catch (error) {
      console.error("Error saving item:", error);
    }
  };

  const handleEdit = (item) => {
    setFormData(item);
    setEditId(item.id);
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this item?")) return;

    try {
      await API.delete(`/inventory/${id}`);
      loadData();
    } catch (error) {
      console.error("Error deleting item:", error);
    }
  };

  return (
    <div className="container">
      <h1>Inventory Management System</h1>

      {summary && (
        <div className="summary-card">
          <h2>Inventory Summary</h2>
          <p>Total Items: {summary.total_items}</p>
          <p>Total RAW Items: {summary.total_raw}</p>
          <p>Total FINISHED Items: {summary.total_finished}</p>
          <p className="low-stock-text">
            Low Stock Items: {summary.low_stock_items}
          </p>
        </div>
      )}

      <div className="form-card">
        <h2>{editId ? "Edit Item" : "Add New Item"}</h2>

        <form onSubmit={handleSubmit} className="form">
          <input
            type="text"
            name="name"
            placeholder="Item Name"
            value={formData.name}
            onChange={handleChange}
            required
          />

          <select
            name="category"
            value={formData.category}
            onChange={handleChange}
          >
            <option value="RAW">RAW</option>
            <option value="FINISHED">FINISHED</option>
          </select>

          <input
            type="number"
            name="quantity"
            placeholder="Quantity"
            value={formData.quantity}
            onChange={handleChange}
            required
          />

          <input
            type="number"
            name="threshold"
            placeholder="Threshold"
            value={formData.threshold}
            onChange={handleChange}
            required
          />

          <input
            type="text"
            name="unit"
            placeholder="Unit (kg, pcs, etc)"
            value={formData.unit}
            onChange={handleChange}
            required
          />

          <div className="button-group">
            <button type="submit" className="primary-btn">
              {editId ? "Update Item" : "Add Item"}
            </button>

            {editId && (
              <button
                type="button"
                className="secondary-btn"
                onClick={resetForm}
              >
                Cancel
              </button>
            )}
          </div>
        </form>
      </div>

      <h2>Inventory List</h2>

      <table className="inventory-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Category</th>
            <th>Quantity</th>
            <th>Threshold</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {inventory.map((item) => (
            <tr
              key={item.id}
              className={item.lowStock ? "low-stock-row" : ""}
            >
              <td>{item.name}</td>
              <td>{item.category}</td>
              <td>{item.quantity}</td>
              <td>{item.threshold}</td>
              <td>
                <span
                  className={
                    item.lowStock ? "status-low" : "status-ok"
                  }
                >
                  {item.lowStock ? "LOW STOCK" : "OK"}
                </span>
              </td>
              <td>
                <button
                  className="edit-btn"
                  onClick={() => handleEdit(item)}
                >
                  Edit
                </button>
                <button
                  className="delete-btn"
                  onClick={() => handleDelete(item.id)}
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;