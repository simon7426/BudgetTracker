import api from "./api";

class TransactionsServiceCategory {
  addCategory({ category_name, category_type }) {
    return api
      .post("/transactions-service/category", {
        category_name,
        category_type,
      })
      .then((response) => {
        return response.data;
      });
  }

  getCategories() {
    return api.get("/transactions-service/category").then((response) => {
      return response.data;
    });
  }

  editCategory({ category_id, category_name, category_type }) {
    return api
      .put(`/transactions-service/category/${category_id}`, {
        category_name,
        category_type,
      })
      .then((response) => {
        return response.data;
      });
  }

  deleteCategory(category_id) {
    return api
      .delete(`/transactions-service/category/${category_id}`)
      .then((response) => {
        return response.status;
      });
  }
}

export default new TransactionsServiceCategory();
