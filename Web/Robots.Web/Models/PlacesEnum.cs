using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Web;

namespace ASP.NET_MVC_Application.Models
{
    public enum Place
    {
        [Description("Aisle 1, Place 1")]
        Aisle1Place1 = 0,
        [Description("Aisle 1, Place 2")]
        Aisle1Place2 = 1,
        [Description("Aisle 1, Place 3")]
        Aisle1Place3 = 2,
        [Description("Aisle 2, Place 1")]
        Aisle2Place1 = 3,
        [Description("Aisle 2, Place 2")]
        Aisle2Place2 = 4,
        [Description("Aisle 2, Place 3")]
        Aisle2Place3 = 5,
        [Description("Aisle 3, Place 1")]
        Aisle3Place1 = 6,
        [Description("Aisle 3, Place 2")]
        Aisle3Place2 = 7,
        [Description("Aisle 3, Place 3")]
        Aisle3Place3 = 8,

        [Description("Robot 1")]
        InTransportation1 = 9,
        [Description("Robot 2")]
        InTransportation2 = 10,

        [Description("Input 1")]
        Coming1 = 11,
        [Description("Input 2")]
        Coming2 = 12,

        [Description("Output 1")]
        Outcome1 = 13,
        [Description("Output 2")]
        Outcome2 = 14,

        [Description("Utillization 1")]
        Utilization1 = 15,
        [Description("Utillization 2")]
        Utilization2 = 16,

        [Description("Empty")]
        Empty1 = 21,
        [Description("Empty")]
        Empty2 = 22,
        [Description("Empty")]
        Empty3 = 23,
        [Description("Empty")]
        Empty4 = 24,
        [Description("Empty")]
        Empty5 = 25,
        [Description("Empty")]
        Empty6 = 26,
        [Description("Empty")]
        Empty7 = 27,
        [Description("Empty")]
        Empty8 = 28,
        [Description("Empty")]
        Empty9 = 29,


    }
}