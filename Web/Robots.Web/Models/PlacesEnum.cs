using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Web;

namespace ASP.NET_MVC_Application.Models
{
    public enum Place
    {
        [Description("Склад 1, Ряд 1")]
        Aisle1Place1 = 0,
        [Description("Склад 1, Ряд 2")]
        Aisle1Place2 = 1,
        [Description("Склад 1, Ряд 3")]
        Aisle1Place3 = 2,
        [Description("Склад 2, Ряд 1")]
        Aisle2Place1 = 3,
        [Description("Склад 2, Ряд 2")]
        Aisle2Place2 = 4,
        [Description("Склад 2, Ряд 3")]
        Aisle2Place3 = 5,
        [Description("Склад 3, Ряд 1")]
        Aisle3Place1 = 6,
        [Description("Склад 3, Ряд 2")]
        Aisle3Place2 = 7,
        [Description("Склад 3, Ряд 3")]
        Aisle3Place3 = 8,

        [Description("Робот 1")]
        InTransportation1 = 9,
        [Description("Робот 2")]
        InTransportation2 = 10,

        [Description("Приход 1")]
        Coming1 = 11,
        [Description("Приход 2")]
        Coming2 = 12,

        [Description("Отгрузка 1")]
        Outcome1 = 13,
        [Description("Отгрузка 2")]
        Outcome2 = 14,

        [Description("Утилизация 1")]
        Utilization1 = 15,
        [Description("Утилизация 2")]
        Utilization2 = 16,

        [Description("Пусто")]
        Empty1 = 21,
        [Description("Пусто")]
        Empty2 = 22,
        [Description("Пусто")]
        Empty3 = 23,
        [Description("Пусто")]
        Empty4 = 24,
        [Description("Пусто")]
        Empty5 = 25,
        [Description("Пусто")]
        Empty6 = 26,
        [Description("Пусто")]
        Empty7 = 27,
        [Description("Пусто")]
        Empty8 = 28,
        [Description("Пусто")]
        Empty9 = 29,


    }
}