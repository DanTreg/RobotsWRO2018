using ASP.NET_MVC_Application.Repositories;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace ASP.NET_MVC_Application.Models
{
    public class ProductPickUpModel
    {
        //public int RobotId { get; set; }
        public string ProductName { get; set; }
        public int Freshness { get; set; }
    }

    public class Machines : Entity
    {
        public MachineStatus MachineIncome { get; set; }
        public MachineStatus MachineOutcome { get; set; }
        public MachineStatus MachineUtilization {get;set;}
    }
}