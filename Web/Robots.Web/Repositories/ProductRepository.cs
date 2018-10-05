using System;
using System.Collections.Generic;
using System.Linq;
using ASP.NET_MVC_Application.Extensions;
using ASP.NET_MVC_Application.Models;

namespace ASP.NET_MVC_Application.Repositories
{
    public class ProductRepository : BaseRepository<Product>
    {
        protected override string EntityName => "Products";

        //Получение списка продуктов 

        public override List<Product> GetAll(bool includeDeleted = false)
        {
            var list = base.GetAll(includeDeleted);
            list.ForEach(x => x.ExpirationStatus = SetExpirationStatus(x.ExpirationDate, x.ExpirationStatus));
            return list;
        }

        //Поиск продукта по имени

        public Product GetByName(string name)
        {
            var all = GetAll();
            var ent = all.Find(x => x.Name == name);
            return ent;
        }


        public int SetExpirationStatus(DateTime ExpirationDate, int currentStatus)
        {
            int result = 1;
            int expirationstatus = 1;
            if (DateTime.Now.Date.AddDays(7) < ExpirationDate.Date && currentStatus != 4)
            {
                expirationstatus = 2;
            }

            if ((DateTime.Now.Date < ExpirationDate.Date) && (ExpirationDate.Date < DateTime.Now.Date.AddDays(7)) && (currentStatus != 4))
            {
                expirationstatus = 3;
            }

            if (DateTime.Now >= ExpirationDate.Date)
            {
                expirationstatus = 4;
            }

            if (currentStatus == 4)
            {
                expirationstatus = 4;
            }

            result = expirationstatus;

            return result;
        }

    }

    //Создание новой записи блокчейн, записи различаются есть или нет айди продукта, в случае Alert айди продукта = null и не участвует в записи

    public class ProductBlockchainRepository : BaseRepository<ProductBlockchain>
    {
        protected override string EntityName => "ProductBlockchain";

        public override ProductBlockchain Create(ProductBlockchain blockchain)
        {
            var rand = new Random(); //рандомное число
            var currentTime = DateTime.Now; //текущее время и дата
            var word = "";
            var last = GetAll().OrderByDescending(x => x.Id).FirstOrDefault(); //получаем хеш последней записи, если есть
            if (blockchain.ProductId is null)
            {
                word = $"{last?.Hash}:{blockchain.Comment}:{currentTime.ToString()}:{rand.ToString()}"; //создаем блокчейн запись
            }
            else
            {
                word = $"{last?.Hash}:{blockchain.Comment}:{blockchain.ProductId}:{currentTime.ToString()}:{rand.ToString()}"; //создаем блокчейн запись
            }
            blockchain.Hash = CryptographyExtensions.GetHashSha256(word);

            return base.Create(blockchain);

        }

    }

    public class RobotRepository : BaseRepository<Robot>
    {
        protected override string EntityName => "Robot";

        //Получение списка продуктов 

        public override List<Robot> GetAll(bool includeDeleted = false)
        {
            var list = base.GetAll(includeDeleted);

            return list;
        }

        //Поиск продукта по имени

        public Robot GetByName(string name)
        {
            var all = GetAll();
            var ent = all.Find(x => x.Name == name);
            return ent;
        }
    }


    public class MachinesRepository : BaseRepository<Machines>
    {
        protected override string EntityName => "Machines";
    }

}