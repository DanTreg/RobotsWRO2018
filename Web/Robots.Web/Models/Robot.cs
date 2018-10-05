using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using Newtonsoft.Json;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel;
using ASP.NET_MVC_Application.Repositories;

namespace ASP.NET_MVC_Application.Models
{
    public class Robot : Entity
    {
        public string Name { get; set; }
        public string Direction { get; set; }
        public int Number { get; set; }
    }

    public class RobotModel : Robot
    {
        public ProductModel Product { get; set; }


    }
}