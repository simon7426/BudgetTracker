import api from "./api";

class TransactionsServiceAccounts {
  addAccount({ account_name, account_type, account_balance }) {
    return api
      .post("/transactions-service/accounts", {
        account_name,
        account_type,
        account_balance,
      })
      .then((response) => {
        return response.data;
      });
  }

  getAccounts() {
    return api.get("/transactions-service/accounts").then((response) => {
      return response.data;
    });
  }

  editAccount({ account_id, account_name, account_type, account_balance }) {
    return api
      .put(`/transactions-service/accounts/${account_id}`, {
        account_name,
        account_type,
        account_balance,
      })
      .then((response) => {
        return response.data;
      });
  }

  deleteAccount(account_id) {
    return api
      .delete(`/transactions-service/accounts/${account_id}`)
      .then((response) => {
        return response.status;
      });
  }
}

export default new TransactionsServiceAccounts();
