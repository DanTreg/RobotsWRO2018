using System;
using System.Web;
using ASP.NET_MVC_Application.Repositories;


namespace ASP.NET_MVC_Application.Models
{
    public class Product : Entity
    {
        public static string ProductFile = HttpContext.Current.Server.MapPath("~/App_Data/Products.json");

        public string Name { get; set; }
        public string Supplier { get; set; }
        public int ExpirationStatus { get; set; }
        public DateTime ExpirationDate { get; set; }
        public Place Place { get; set; }
        public string Reason { get; set; }
        public string Destination { get; set; }

    }


}