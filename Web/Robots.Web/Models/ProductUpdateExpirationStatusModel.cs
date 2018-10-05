using System;

namespace ASP.NET_MVC_Application.Models
{
    public class ProductUpdateExpirationStatusModel
    {
        public int ProductId { get; set; }
        public int ExpirationStatus { get; set; }
        public string Reason { get; set; }
    }
}