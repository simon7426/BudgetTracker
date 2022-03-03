import api from "./api";

class TransactionsService {
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
}

export default new TransactionsService();
