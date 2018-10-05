using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace ASP.NET_MVC_Application.Models
{
    public class MainModel
    {
        public MainModel()
        {
            Products = new List<ProductModel>();
        }



        public List<ProductModel> Products { get; set; }
        public RobotModel Robot1 { get; set; }
        public RobotModel Robot2 { get; set; }

        public MachineStatus MachineIncome { get; set; }
        public MachineStatus MachineUtilization { get; set; }
        public MachineStatus MachineOutcome { get; set; }

        public bool IsPartial { get; set; }
    }

    public enum MachineStatus
    {
        No = 0,
        Came = 1,
        Gone = 2
    }

    public class ProductModel : Product
    {
        public ProductModel()
        {
            ProductBlockchains = new List<ProductBlockchain>();
        }

        public List<ProductBlockchain> ProductBlockchains { get; set; }

        public TransportationChain LastTransportationChain => ProductBlockchains.LastOrDefault(x=>x.TransportationChain != null)?.TransportationChain;
    }
}