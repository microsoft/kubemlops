output "mysql_name" {
    description = "name of the mysql server"
    value = azurerm_mysql_server.this.name
}