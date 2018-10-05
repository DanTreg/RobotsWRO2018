using ASP.NET_MVC_Application.Repositories;

namespace ASP.NET_MVC_Application.Models
{
    public class ProductBlockchain : Entity
    {
        public int? ProductId { get; set; }
        public string Comment { get; set; }
        public string Hash { get; set; }
        public TransportationChain TransportationChain { get; set; }
    }


    public class ProductBlockchainModel
    {
        public string ProductName { get; set; }
        public string Comment { get; set; }
        public TransportationChain TransportationChain { get; set; }
    }
}